# Generated by Django 5.1.4 on 2024-12-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_withdrawal_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='phone_number',
            field=models.CharField(default='00000000000', max_length=15),
            preserve_default=False,
        ),
    ]