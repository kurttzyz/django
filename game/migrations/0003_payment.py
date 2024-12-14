# Generated by Django 5.1.4 on 2024-12-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_remove_bet_game_alter_bet_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference_number', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
