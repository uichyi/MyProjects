# Generated by Django 4.2.5 on 2023-11-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0005_alter_user_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.AddField(
            model_name='post',
            name='username',
            field=models.CharField(blank=True, help_text='Username', max_length=20, null=True, verbose_name='username'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]