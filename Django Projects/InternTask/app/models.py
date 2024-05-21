from django.db import models

# Create your models here.


class DBUser(models.Model):
    fullName = models.CharField(max_length=60, help_text="ФИО")
    username = models.CharField(max_length=20, help_text="Логин")
    password = models.CharField(max_length=20, help_text="Пароль")

    def __str__(self):
        return self.fullName.__str__()


class Client(models.Model):
    statusOptions = [
        ("not_active", "Не в работе"),
        ("in_process", "В работе"),
        ("rejection", "Отказ"),
        ("deal_closed", "Сделка закрыта"),
    ]

    accountNumber = models.CharField(max_length=20, help_text="Номер Счета")
    surname = models.CharField(max_length=20, help_text="Фамилия")
    name = models.CharField(max_length=20, help_text="Имя")
    patronymic = models.CharField(max_length=20, help_text="Отчество")
    birthday = models.DateField(help_text="Дата Рождения")
    # TIN = ИНН
    TIN = models.CharField(max_length=12, help_text="ИНН")
    responsible = models.ForeignKey(DBUser, on_delete=models.CASCADE, help_text="ФИО Ответственного")
    status = models.CharField(max_length=20, choices=statusOptions, default="not_active", help_text="Статус")

    def __str__(self):
        return self.accountNumber.__str__()

