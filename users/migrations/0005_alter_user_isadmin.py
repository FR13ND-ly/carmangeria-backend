# Generated by Django 5.0.2 on 2024-02-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_isadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]
