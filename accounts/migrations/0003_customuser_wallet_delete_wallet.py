# Generated by Django 5.1.4 on 2024-12-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_wallet_balance_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]