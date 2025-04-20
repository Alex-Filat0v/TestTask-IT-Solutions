from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from entries.models import Status, Type, Category, Subcategory, Entry, CategoryLinksType
from entries.forms import EntryForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm, CategoryLinksTypeForm
from django.urls import reverse
from django.utils.dateparse import parse_date


def home(request):
    """
    View для отображения главной страницы с фильтрацией записей.
    :param request:
    :return:
    """
    # Получаем все записи текущего пользователя, чтобы остальные не могли увидеть его записи.
    entries = Entry.objects.filter(user_id=request.user.id)

    # Получаем значения фильтров из GET запроса, если такие есть
    date_from = parse_date(request.GET.get('date_from')) if request.GET.get('date_from') else None
    date_to = parse_date(request.GET.get('date_to')) if request.GET.get('date_to') else None
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    # Применяем все полученные фильтры для записей.
    if date_from:
        entries = entries.filter(date__gte=date_from)
    if date_to:
        entries = entries.filter(date__lte=date_to)
    if status_id:
        entries = entries.filter(status_id=status_id)
    if type_id:
        entries = entries.filter(type_id=type_id)
    if category_id:
        entries = entries.filter(category_id=category_id)
    if subcategory_id:
        entries = entries.filter(subcategory_id=subcategory_id)

    # Передаем все данные для отображения таблицы в контекст и возвращаем его для вывода пользователю.
    context = {
        'entries': entries,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }

    return render(request, 'entries/home.html', context=context)


def form(request):
    """
    View для отображения формы создания новой записи.
    :param request:
    :return:
    """
    # Если пользователь не авторизован - он не может создавать записи, перенаправляем его на главную страницу.
    if not request.user.id:
        return HttpResponseRedirect(reverse('home'))

    # Получаем данные из POST запроса, если он был отправлен
    data = request.POST if request.method == 'POST' else None
    entry_form = EntryForm(data)

    selected_type = data.get('type') if data else None
    selected_category = data.get('category') if data else None

    # Устанавливаем доступные категории в зависимости от выбранного типа пользователям с помощью таблицы связей
    # category_links_type.
    if selected_type:
        linked_categories = CategoryLinksType.objects.filter(type_id=selected_type).values_list('category_id', flat=True)
        entry_form.fields['category'].queryset = Category.objects.filter(id__in=linked_categories)

    # Устстанавливаем для пользователя доступные подкатегории для выбранной категории с помошью внешнего ключа
    # category_id в таблице subcategory.
    if selected_category:
        entry_form.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=selected_category)

    # Проверяем чтобы пользователь отправил все данные.
    if request.method == 'POST' and all([data.get('status'), data.get('type'), data.get('category'),
                                         data.get('subcategory'), data.get('amount'), data.get('date')]):
        # Проводим валидацию данных, которые отправил пользователь, если она прошла - создаем новую запись.
        if entry_form.is_valid():

            Entry.objects.create(
                user=request.user,
                date=entry_form.cleaned_data['date'],
                status=entry_form.cleaned_data['status'],
                type=entry_form.cleaned_data['type'],
                category=entry_form.cleaned_data['category'],
                subcategory=entry_form.cleaned_data['subcategory'],
                amount=entry_form.cleaned_data['amount'],
                comment=entry_form.cleaned_data['comment']
            )
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'entries/entries_form.html', {'form': entry_form})


def edit_entry(request, entry_id):
    """
    View для редактирования или удаления записи.
    :param request:
    :param entry_id: ID записи для редактирования
    :return:
    """
    entry = get_object_or_404(Entry, pk=entry_id)

    # Проверяем является ли пользователь создателем записи, если нет - перенаправляем его на домашнюю страницу.
    if entry.user != request.user:
        return HttpResponseRedirect(reverse('home'))

    # Получаем данные из POST запроса, если он был отправлен.
    if request.method == 'POST':

        # Если запрос был на удаление записи - удаляем запись и перенаправляем пользователя на домашнюю страницу.
        if 'delete' in request.POST:
            entry.delete()
            return HttpResponseRedirect(reverse('home'))

        # Создаем форму с переданными данными
        form = EntryForm(request.POST)

        # Получаем выбранные пользователем значения типа и категории.
        selected_type = request.POST.get('type')
        selected_category = request.POST.get('category')

        # Обновляем доступные категории и подкатегории в зависимости выбранного типа и категории.
        if selected_type:
            linked_categories = CategoryLinksType.objects.filter(type_id=selected_type).values_list('category_id', flat=True)
            form.fields['category'].queryset = Category.objects.filter(id__in=linked_categories)
        if selected_category:
            form.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=selected_category)

        # Если запрос был на созранени данных.
        if 'save' in request.POST:
            # Проводим валидацию данных.
            if form.is_valid():
                entry.date = form.cleaned_data['date']
                entry.status = form.cleaned_data['status']
                entry.type = form.cleaned_data['type']
                entry.category = form.cleaned_data['category']
                entry.subcategory = form.cleaned_data['subcategory']
                entry.amount = form.cleaned_data['amount']
                entry.comment = form.cleaned_data['comment']

                # Сохраняем запись и возвращаем пользователя на домашнюю страницу.
                entry.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'entries/edit_entry_form.html', {'form': form, 'entry': entry})

    else:
        # Заполняем форму данными из записи.
        initial_data = {
            'date': entry.date.strftime('%Y-%m-%d'),
            'status': entry.status,
            'type': entry.type,
            'category': entry.category,
            'subcategory': entry.subcategory,
            'amount': entry.amount,
            'comment': entry.comment
        }
        form = EntryForm(initial=initial_data)

        selected_type = entry.type.id
        selected_category = entry.category.id

        # Обновляем доступные категории и подкатегории в зависимости от записи
        if selected_type:
            linked_categories = CategoryLinksType.objects.filter(type_id=selected_type).values_list('category_id', flat=True)
            form.fields['category'].queryset = Category.objects.filter(id__in=linked_categories)
        if selected_category:
            form.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=selected_category)

    return render(request, 'entries/edit_entry_form.html', {'form': form, 'entry': entry})


def dictionaries(request):
    """
    View для управления справочниками для редактирования статусов, типов, категорий, подкатегорий и связей между
     типами и категориями.
    :param request:
    :return:
    """
    # Если пользователь не авторизован - отправляем его на главную страницу
    if not request.user.id:
        return HttpResponseRedirect(reverse('home'))

    # Получаем данные о всех имеющихся статусах, типах, категориях, подкатегориях и связях между типами и категориями.
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    category_links = CategoryLinksType.objects.select_related('type', 'category')

    # Добавляем эти данные в контекст и возвращаем в рендер страницы.
    context = {
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        'category_links': category_links,
    }
    return render(request, 'entries/dictionaries.html', context=context)


def edit_dictionary_item(request, item_type, item_id):
    """
    View для редактирования или удаления элемента из справочников.
    :param request:
    :param item_type: Тип элемента (статус, тип, категория, подкатегория, связи между типами и категориями)
    :param item_id: id элемента для редактирования или удаления
    :return:
    """

    # Если пользователь не авторизован - отправляем его на главную страницу
    if not request.user.id:
        return HttpResponseRedirect(reverse('home'))

    # Получаем нужную форму по типу элемента.
    form_class = {
        'status': StatusForm,
        'type': TypeForm,
        'category': CategoryForm,
        'subcategory': SubcategoryForm,
        'link': CategoryLinksTypeForm,
    }.get(item_type)

    # Получаем нужную модель по типу элемента.
    model_class = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory,
        'link': CategoryLinksType,
    }.get(item_type)

    # Если тип элемента не распознан - возвращаем пользователя на страницу со справочниками.
    if not form_class or not model_class:
        return HttpResponseRedirect(reverse('dictionaries'))

    instance = None
    if item_id != 0:
        # Если редактируем существующий элемент - получаем его из базы.
        instance = get_object_or_404(model_class, id=item_id)

        # Если нажата кнопка удаления - удаляем элемент и возвращаемся на страницу справочников.
        if request.method == 'POST' and 'delete' in request.POST:
            instance.delete()
            return HttpResponseRedirect(reverse('dictionaries'))

    # Если форма отправлена не на удаление.
    if request.method == 'POST' and 'delete' not in request.POST:
        form = form_class(request.POST, instance=instance)

        # Если форма валидна - сохраняем данные и возвращаемся к справочникам.
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dictionaries'))
    else:
        form = form_class(instance=instance)

    # Для отображения названия типа элементов в шаблоне
    item_type_verbose = {
        'status': 'статус',
        'type': 'тип',
        'category': 'категорию',
        'subcategory': 'подкатегорию',
        'link': 'связь',
    }.get(item_type, 'элемент')

    # Добавляем эти данные в контекст и возвращаем в рендер страницы.
    context = {
        'form': form,
        'item_type_verbose': item_type_verbose,
        'is_edit': item_id != 0,
    }
    return render(request, 'entries/edit_dictionary_item.html', context)
