# Generated by Django 5.1.4 on 2024-12-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_withdrawal_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
