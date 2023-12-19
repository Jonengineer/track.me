# Generated by Django 5.0 on 2023-12-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='track_map',
            fields=[
                ('track_map_id', models.AutoField(primary_key=True, serialize=False)),
                ('track_coordinat', models.JSONField()),
                ('gpxtrek', models.FileField(upload_to='gpx_tracks/')),
            ],
            options={
                'db_table': 'track_map',
                'managed': True,
            },
        ),
    ]
