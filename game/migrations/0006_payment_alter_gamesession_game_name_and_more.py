# Generated by Django 5.1.4 on 2024-12-10 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_rename_date_played_gamesession_start_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.AlterField(
            model_name='gamesession',
            name='game_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
