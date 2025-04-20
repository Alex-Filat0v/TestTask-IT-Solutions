from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя, наследуется от AbstractUser.
    В этой модели мы можем добавлять свои методы или свойства, если они нужны.
    """

    def __str__(self):
        """
        Переопределение метода __str__ для удобства отображения имени пользователя в админ-панели.
        """
        return self.username
