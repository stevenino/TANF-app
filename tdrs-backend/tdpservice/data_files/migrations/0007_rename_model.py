# Generated by Django 3.2.3 on 2021-05-24 19:06
from django.db import migrations, models
import tdpservice.data_files.models

class Migration(migrations.Migration):

    dependencies = [
        ('data_files', '0006_datafile_file'),
    ]

    operations = [
        migrations.AlterModelTable(
            'DataFile',
            'data_files_datafile'
        )
    ]
