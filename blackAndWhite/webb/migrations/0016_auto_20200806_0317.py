# Generated by Django 3.0.6 on 2020-08-06 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0014_remove_creator_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uploaded',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webb.Profile'),
        ),
        # migrations.AlterField(
        #     model_name='product',
        #     name='creator',
        #     field=models.CharField(max_length=100),
        # ),
    ]
