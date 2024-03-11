# Generated by Django 3.2.25 on 2024-03-11 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('card', 'Карта'), ('cash', 'Наличные'), ('sbp', 'СБП')], default='cash', max_length=100),
        ),
    ]
