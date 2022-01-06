# Generated by Django 4.0 on 2022-01-05 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(blank=True, choices=[('PAID', 'Paid'), ('PEND', 'pending'), ('APPR', 'approved'), ('CANC', 'Canceled')], default='PEND', max_length=4, null=True),
        ),
    ]