# Generated by Django 3.0.6 on 2020-08-06 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0013_auto_20200805_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creator',
            name='skills',
        ),
    ]
