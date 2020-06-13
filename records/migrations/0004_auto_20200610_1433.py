# Generated by Django 3.0.3 on 2020-06-10 05:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20200610_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='recommended',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='おすすめ度'),
        ),
    ]
