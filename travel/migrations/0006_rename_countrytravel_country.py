# Generated by Django 4.2.6 on 2023-12-16 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_rename_country_countrytravel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='countrytravel',
            new_name='country',
        ),
    ]
