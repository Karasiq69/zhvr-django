# Generated by Django 3.2.25 on 2024-03-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20240307_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, help_text='Обязательное поле', max_length=255, unique=True, verbose_name='Название категории'),
        ),
    ]
