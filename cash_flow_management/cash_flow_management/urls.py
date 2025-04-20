"""
URL configuration for cash_flow_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
Основной каталог, где храним ссылки и имена для них.
"""

from django.contrib import admin
from django.urls import path, include
from entries.views import home, form, dictionaries, edit_entry, edit_dictionary_item


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authorization.urls', namespace='authorization')),
    path('', home, name='home'),
    path('?date_from=&date_to=&status=&type=&category=&subcategory=', home, name='home'),
    path('form/', form, name='form'),
    path('edit/<int:entry_id>/', edit_entry, name='edit_entry'),
    path('dictionaries/', dictionaries, name='dictionaries'),
    path('dictionaries/<str:item_type>/<int:item_id>/', edit_dictionary_item, name='edit_dictionary_item'),
]
