# Generated by Django 4.2.6 on 2023-12-16 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_alter_country_namecountry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='country',
        ),
    ]
