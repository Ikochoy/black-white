# Generated by Django 3.0.6 on 2020-08-20 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0024_auto_20200819_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
