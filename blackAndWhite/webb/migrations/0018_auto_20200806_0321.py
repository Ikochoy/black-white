# Generated by Django 3.0.6 on 2020-08-06 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0017_auto_20200806_0320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='uploaded',
            new_name='uploader',
        ),
    ]
