# Generated by Django 4.2.20 on 2025-04-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0011_userprofile_delete_usermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
