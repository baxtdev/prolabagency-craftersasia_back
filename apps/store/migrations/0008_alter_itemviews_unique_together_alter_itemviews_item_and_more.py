# Generated by Django 5.0.2 on 2024-04-29 06:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_itemviews_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemviews',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='itemviews',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='store.item'),
        ),
        migrations.AlterUniqueTogether(
            name='itemviews',
            unique_together={('user', 'item')},
        ),
    ]