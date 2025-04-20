from django.contrib import admin
from authorization.models import User


"""
Регистрируем таблицу User для стандартной админ-панели в Django
"""
admin.site.register(User)
