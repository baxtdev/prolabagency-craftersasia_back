# Generated by Django 5.0.2 on 2024-04-08 05:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0002_initial'),
        ('order', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.color'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='companies.company', verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.item', verbose_name='Товара'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='item_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.itemmodel', verbose_name='Модель Товара'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='Товары заказа'),
        ),
    ]