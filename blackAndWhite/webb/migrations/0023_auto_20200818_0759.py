# Generated by Django 3.0.6 on 2020-08-18 07:59

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0022_auto_20200813_0145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-uploaded_date',)},
        ),
        migrations.AddField(
            model_name='coupon',
            name='expire_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]