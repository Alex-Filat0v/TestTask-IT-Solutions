from django.urls import path

from authorization.views import login, registration, logout

app_name = 'authorization'

# Регистрируем отдельные ссылки для приложения регистрации и авторизации.
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', registration, name='register'),
    path('logout/', logout, name='logout'),
]
