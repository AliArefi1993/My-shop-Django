# Generated by Django 4.0 on 2022-01-08 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='post',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]