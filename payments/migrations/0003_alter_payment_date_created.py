# Generated by Django 5.1.4 on 2024-12-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_payment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
