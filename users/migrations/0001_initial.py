# Generated by Django 4.1.2 on 2022-10-27 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=None, max_length=150, verbose_name='user_id')),
            ],
            options={
                'verbose_name': 'user_id',
                'verbose_name_plural': 'user_ids',
            },
        ),
    ]
