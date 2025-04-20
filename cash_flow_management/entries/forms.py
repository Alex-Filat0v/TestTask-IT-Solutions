from django import forms
from django.utils import timezone
from entries.models import Status, Type, Category, Subcategory, Entry, CategoryLinksType


class EntryForm(forms.Form):
    """
    Форма для создания или редактирования записи.
    Содержит поля для выбора даты, статуса, типа, категории, подкатегории, суммы и комментария.
    """

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date()
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'submit();'}),
        required=True,
        label='Тип'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'submit();'}),
        required=False,
        label='Категория'
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Подкатегория'
    )
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Entry
        fields = ('date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class StatusForm(forms.ModelForm):
    """
    Форма для создания или редактирования статуса записи.
    """

    class Meta:
        model = Status
        fields = ('status_name',)
        labels = {'status_name': 'Статус'}
        widgets = {
            'status_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TypeForm(forms.ModelForm):
    """
    Форма для создания или редактирования типа записи.
    """

    class Meta:
        model = Type
        fields = ('type_name',)
        labels = {'type_name': 'Тип'}
        widgets = {
            'type_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    """
    Форма для создания или редактирования категории записи.
    """

    class Meta:
        model = Category
        fields = ('category_name',)
        labels = {'category_name': 'Категория'}
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class SubcategoryForm(forms.ModelForm):
    """
    Форма для создания или редактирования подкатегории записи.
    Включает выбор категории и название подкатегории.
    """

    class Meta:
        model = Subcategory
        fields = ('category', 'subcategory_name',)
        labels = {
            'category': 'Категория',
            'subcategory_name': 'Подкатегория'
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryLinksTypeForm(forms.ModelForm):
    """
    Форма для связывания типа и категории.
    """

    class Meta:
        model = CategoryLinksType
        fields = ('type', 'category',)
        labels = {
            'type': 'Тип',
            'category': 'Категория'
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
