from django.db import models
from authorization.models import User


class Status(models.Model):
    """
    Модель для статуса записи.
    """

    # Имя статуса, уникальное для каждой записи.
    status_name = models.TextField(unique=True)

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения статуса в админ-панели.
        """
        return self.status_name


class Category(models.Model):
    """
    Модель для категории.
    """

    # Имя категории, уникальное для каждой записи.
    category_name = models.TextField(unique=True)

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения названия категории в админ-панели.
        """
        return self.category_name


class Subcategory(models.Model):
    """
    Модель для подкатегории.
    Подкатегория привязана к категории и с помощью ForeignKey и таким образом выбрав одну из категорий мы не сможем
    выбрать подкатегорию, которая не пренадлежит ей.
    """

    # Название подкатегории, уникальное для каждой записи, чтобы не было 2 одинаковых подкатегорий.
    subcategory_name = models.TextField(unique=True)
    # Ставим каскадное удаление, чтобы при удалении категории также и удалялись все привязанные к ней категории.
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения названия подкатегории в админ-панели.
        """
        return self.subcategory_name


class Type(models.Model):
    """
    Модель для типа записи.
    """

    # Название типа записи уникальное.
    type_name = models.TextField(unique=True)

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения названия типа в админ-панели.
        """
        return self.type_name


class CategoryLinksType(models.Model):
    """
    Модель для связи между типами и категориями, чтобы к одному типу могло относится несколько категорий, так же как и к
    одной категории могли относится сразу несколько типов.

    Ставим каскадное удаление, чтобы при удалении типа или категории также и удалялись все записи о связях с удаленным
    значением.
    """

    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения информации о типе и категории в админ-панели.
        """
        return f'К типу: {self.type.type_name} относится категория: {self.category.category_name}'


class Entry(models.Model):
    """
    Модель, описывающая основную стуктуру проекта - запись.
    Это основная модель для хранения информации о движении денежных средств.

    Включает в себя:
    пользователя, который создал эту запись, дату, статус, тип, категорию, подкатегорию, сумму и комментарий.

    Каскадное удаление, в случае удаления, например, типа, удалятся также все записи с этим типом.
    Тут желательно бы ставить PROTECT!
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.ForeignKey(to=Status, on_delete=models.CASCADE)
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(to=Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    comment = models.TextField(null=True, blank=True)

