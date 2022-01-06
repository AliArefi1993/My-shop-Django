# Generated by Django 4.0 on 2022-01-01 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_supplier_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supplier_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]