# Generated by Django 4.0 on 2021-12-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='post_code',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='city',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='country',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='post_code',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='state',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
    ]
