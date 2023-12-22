# Generated by Django 4.2.5 on 2023-10-29 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Board's name", max_length=25, verbose_name='Board title')),
            ],
            options={
                'db_table': 'Board',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Username', max_length=20, verbose_name='username')),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Thread's name", max_length=50, verbose_name='Thread title')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageboard.board')),
            ],
            options={
                'db_table': 'Thread',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(help_text='Post content', max_length=500, verbose_name='text')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageboard.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageboard.user')),
            ],
            options={
                'db_table': 'Post',
            },
        ),
    ]
