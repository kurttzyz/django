# Generated by Django 5.1.1 on 2024-12-08 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='game',
        ),
        migrations.AlterField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser'),
        ),
    ]
