# Generated by Django 3.2 on 2021-04-23 14:17

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import engine.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Заголовок', max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('slug', autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from=engine.models.Ticket.function, slugify=engine.models.Ticket.function1, unique_with=['id', 'created'])),
                ('description', models.CharField(help_text='Описание проблемы', max_length=15000)),
                ('resolution', models.CharField(help_text='Решение проблемы', max_length=15000)),
                ('priority', models.IntegerField(blank=True, choices=[(1, '1. Критический'), (2, '2. Высокий'), (3, '3. Нормальный'), (4, '4. Низкий'), (5, '5. Очень низкий')], default=3, help_text='Приоритет', verbose_name='Priority')),
                ('email_address', models.EmailField(blank=True, help_text='Email', max_length=254, null=True)),
                ('status', models.CharField(blank=True, choices=[('Open', 'Открытый'), ('Resolved', 'На рассмотрении'), ('Closed', 'Закрытый')], default='Open', help_text='Статус', max_length=20, verbose_name='Status')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UpdatedTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Resolve', models.CharField(max_length=1500)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.ticket', verbose_name='UpdatedTicket')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
