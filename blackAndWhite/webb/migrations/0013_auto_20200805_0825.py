# Generated by Django 3.0.6 on 2020-08-05 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webb', '0012_auto_20200731_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creator',
            name='social_media_url',
        ),
        migrations.CreateModel(
            name='SocialMediaUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(choices=[('twitter', 'twitter'), ('instagram', 'instagram'), ('pininterest', 'pininterest'), ('facebook', 'facebook')], max_length=30)),
                ('url', models.CharField(max_length=200)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webb.Creator')),
            ],
        ),
    ]