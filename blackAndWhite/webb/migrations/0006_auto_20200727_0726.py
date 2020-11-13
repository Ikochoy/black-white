# Generated by Django 3.0.6 on 2020-07-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0005_auto_20200727_0510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='critiqueimage',
            name='critique',
        ),
        migrations.AddField(
            model_name='blog',
            name='cover_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='blogs_critiques_covers/'),
        ),
        migrations.AddField(
            model_name='critique',
            name='cover_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='blogs_critiques_covers/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pic',
            field=models.ImageField(upload_to='products/'),
        ),
        migrations.DeleteModel(
            name='BlogImage',
        ),
        migrations.DeleteModel(
            name='CritiqueImage',
        ),
    ]