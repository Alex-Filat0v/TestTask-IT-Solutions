from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from authorization.forms import AuthorizationForm, RegistrationForm
from entries.models import Entry


def login(request):
    """
    View для авторизации пользователя.
    :param request:
    :return:
    """
    # Если был отправлен POST запрос, то оздаем форму с данными из запроса.
    if request.method == 'POST':
        form = AuthorizationForm(data=request.POST)

        # Проводим валидацию данных из формы.
        if form.is_valid():

            # Получаем введенные пользователям данные.
            username = request.POST['username']
            password = request.POST['password']

            # Проводим попытку аутентификации пользователя.
            user = auth.authenticate(username=username, password=password)

            # Если пользователь найден - авторизуем пользователя и перенаправляем на домашнюю страницу.
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))

    # Если был отправлен GET запрос - создаем пустую форму.
    else:
        form = AuthorizationForm()

    context = {'form': form, 'entries': Entry.objects.all()}
    return render(request, 'authorization/login.html', context)


def registration(request):
    """
    View для регистрации нового пользователя
    :param request:
    :return:
    """
    # Если был отправлен POST запрос, то оздаем форму с данными из запроса.
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)

        # Проводим валидацию данных из формы.
        if form.is_valid():
            # Сохраняем данные нового пользователя, отправляем сообщение об успешной регистрации и
            # перенаправляем на страницу входа.
            form.save()
            messages.success(request, 'Регистрация прошла успешно')
            return HttpResponseRedirect(reverse('authorization:login'))

    # Если был отправлен GET запрос - создаем пустую форму.
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'authorization/register.html', context)


def logout(request):
    """
    View для выхода пользователя
    :param request:
    :return:
    """
    # Осуществляем logout пользователя и перенаправляем на домашнюю страницу
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))
