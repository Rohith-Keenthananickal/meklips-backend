# Generated by Django 5.1.7 on 2025-05-29 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_passwordresetotp_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetotp',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
