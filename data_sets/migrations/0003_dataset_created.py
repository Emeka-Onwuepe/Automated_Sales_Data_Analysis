# Generated by Django 4.1.2 on 2022-12-01 06:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_sets', '0002_dataset_columns'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
    ]
