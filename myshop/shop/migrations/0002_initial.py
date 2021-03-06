# Generated by Django 4.0 on 2022-01-13 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='custom_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.type'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shop.tag'),
        ),
    ]
