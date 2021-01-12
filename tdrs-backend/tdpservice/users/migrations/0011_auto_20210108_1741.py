# Generated by Django 3.1.4 on 2021-01-08 17:41

from django.contrib.auth.models import Group
from django.db import migrations


def remove_groups(apps, schema_editor):
    Group.objects.filter(name__in={"OFA Analyst"}).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_user_roles'),
    ]

    operations = [
        migrations.RunPython(remove_groups),
    ]
