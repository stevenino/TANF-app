# Generated by Django 3.2.1 on 2021-05-20 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_sub'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deactivated',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='deactivated'),
        ),
    ]