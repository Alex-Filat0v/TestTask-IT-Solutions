from django.contrib import admin
from entries.models import Status, Type, Category, Subcategory, Entry, CategoryLinksType


"""
Регистрируем таблицы Status, Type, Category, Subcategory, Entry, CategoryLinksType 
для стандартной админ-панели в Django
"""
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Entry)
admin.site.register(CategoryLinksType)
