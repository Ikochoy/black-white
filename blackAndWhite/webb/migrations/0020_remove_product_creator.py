# Generated by Django 3.0.6 on 2020-08-06 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0019_auto_20200806_0322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='creator',
        ),
    ]
