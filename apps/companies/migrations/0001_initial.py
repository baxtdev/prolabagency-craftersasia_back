# Generated by Django 5.0.2 on 2024-04-08 05:24

import django.core.validators
import django_resized.forms
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('legal_name', models.CharField(max_length=350, verbose_name='Название')),
                ('legal_address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Aдрес')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('index', models.PositiveIntegerField(verbose_name='Индекс')),
                ('site_url', models.URLField(blank=True, null=True, verbose_name='Ссылка сайта')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=90, scale=None, size=[1920, 1080], upload_to='avatars/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
                'db_table': 'companies',
                'ordering': ('-created_at', '-updated_at', '-id'),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CompanyApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('legal_name', models.CharField(max_length=350, verbose_name='Название')),
                ('legal_address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Aдрес')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('index', models.PositiveIntegerField(verbose_name='Индекс')),
                ('site_url', models.URLField(blank=True, null=True, verbose_name='Ссылка сайта')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=90, scale=None, size=[1920, 1080], upload_to='avatars/', verbose_name='Фото')),
                ('is_approved', models.BooleanField(default=False, help_text='Чтобы принимать заявку установите этот флажок', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заявка на открытие магазина',
                'verbose_name_plural': 'Заявки на открытие магазинов',
                'db_table': 'store_aplications',
                'ordering': ('-created_at', '-updated_at', '-id'),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CompanyBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма депозита')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма продажи')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Депозит Баланс компании',
                'verbose_name_plural': 'Депозиты Баланс компаний',
                'db_table': 'company_deposits',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CompanyPayAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('payment_type', models.CharField(choices=[('MBANK', 'МБАНК'), ('VISA', 'VISA'), ('WITH_OUT', 'Без оплаты')], default='WITH_OUT', max_length=15, verbose_name='Тип оплаты')),
                ('api_key', models.CharField(max_length=255)),
                ('bank_account', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Счет Компании для Оплаты ',
                'verbose_name_plural': 'Счета Компании для Оплаты',
                'db_table': '',
                'ordering': ('-id', 'created_at'),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RateComission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350, verbose_name='Название')),
                ('comission_percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процент')),
            ],
        ),
    ]
