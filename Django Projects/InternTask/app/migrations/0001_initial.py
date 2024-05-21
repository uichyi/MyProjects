# Generated by Django 5.0.4 on 2024-04-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.CharField(help_text='Номер Счета', max_length=20)),
                ('surname', models.CharField(help_text='Фамилия', max_length=20)),
                ('name', models.CharField(help_text='Имя', max_length=20)),
                ('patronymic', models.CharField(help_text='Отчество', max_length=20)),
                ('birthday', models.DateField(help_text='Дата Рождения')),
                ('TIN', models.CharField(help_text='ИНН', max_length=12)),
                ('responsible', models.CharField(help_text='ФИО Ответственного', max_length=60)),
                ('status', models.CharField(choices=[('not_active', 'Не в работе'), ('in_process', 'В работе'), ('rejection', 'Отказ'), ('deal_closed', 'Сделка закрыта')], default='not_active', help_text='Статус', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(help_text='ФИО', max_length=60)),
                ('username', models.CharField(help_text='Логин', max_length=20)),
                ('password', models.CharField(help_text='Пароль', max_length=20)),
            ],
        ),
    ]