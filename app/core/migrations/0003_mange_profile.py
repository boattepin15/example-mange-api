# Generated by Django 3.2.25 on 2024-06-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_mange'),
    ]

    operations = [
        migrations.AddField(
            model_name='mange',
            name='profile',
            field=models.ImageField(default='default.jpg', upload_to='mange_profiles/'),
        ),
    ]
