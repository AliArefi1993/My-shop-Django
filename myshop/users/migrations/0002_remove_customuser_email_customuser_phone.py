# Generated by Django 4.0 on 2021-12-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=9301605684, max_length=11, unique=True),
            preserve_default=False,
        ),
    ]
