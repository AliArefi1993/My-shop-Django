# Generated by Django 4.0 on 2022-01-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_delete_customer'),
        ('order', '0006_orderitem_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(through='order.OrderItem', to='shop.Product'),
        ),
    ]
