# Generated by Django 4.0 on 2022-01-11 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='items',
        ),
    ]