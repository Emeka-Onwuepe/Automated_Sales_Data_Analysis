# Generated by Django 4.1.2 on 2022-10-23 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_id', models.CharField(blank=None, max_length=150, verbose_name='dataset_id')),
                ('dataset', models.FileField(upload_to='', verbose_name='dataset')),
                ('report_title', models.FileField(upload_to='', verbose_name='report title')),
                ('currency_symbol', models.FileField(upload_to='', verbose_name='currency symbol')),
                ('zipfolder', models.FileField(blank=True, upload_to='', verbose_name='zipfolder')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_user_id', to='users.user_id')),
            ],
            options={
                'verbose_name': 'Dataset',
                'verbose_name_plural': 'Datasets',
            },
        ),
    ]
