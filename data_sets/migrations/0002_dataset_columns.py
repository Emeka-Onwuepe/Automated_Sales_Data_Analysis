# Generated by Django 4.1.2 on 2022-10-28 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_sets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='columns',
            field=models.TextField(blank=True, verbose_name='columns'),
        ),
    ]
