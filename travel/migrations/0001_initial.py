# Generated by Django 4.2.6 on 2023-12-13 21:15

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('namebooking', models.CharField(max_length=60)),
                ('datestart', models.DateTimeField()),
                ('datefinish', models.DateTimeField()),
                ('adress', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'booking',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='description',
            fields=[
                ('descriptiond_id', models.AutoField(primary_key=True, serialize=False)),
                ('title_descriptiond', models.CharField(max_length=100)),
                ('name_descriptiond', models.CharField(max_length=6000)),
                ('media_1', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_1', models.CharField(blank=True, max_length=200, null=True)),
                ('media_2', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_2', models.CharField(blank=True, max_length=200, null=True)),
                ('media_3', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_3', models.CharField(blank=True, max_length=200, null=True)),
                ('media_4', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_4', models.CharField(blank=True, max_length=200, null=True)),
                ('media_5', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_5', models.CharField(blank=True, max_length=200, null=True)),
                ('media_6', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_6', models.CharField(blank=True, max_length=200, null=True)),
                ('media_7', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_7', models.CharField(blank=True, max_length=200, null=True)),
                ('media_8', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_8', models.CharField(blank=True, max_length=200, null=True)),
                ('media_9', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_9', models.CharField(blank=True, max_length=200, null=True)),
                ('media_10', models.CharField(blank=True, max_length=200, null=True)),
                ('description_media_10', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'description',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='point_trek',
            fields=[
                ('point_trek_id', models.AutoField(primary_key=True, serialize=False)),
                ('namepoint', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=400)),
                ('point_сoordinates', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'point_trek',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='sight',
            fields=[
                ('sight_id', models.AutoField(primary_key=True, serialize=False)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('url', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'sight',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('typeticket', models.CharField(max_length=40)),
                ('datestart', models.DateTimeField()),
                ('datefinish', models.DateTimeField()),
                ('adressstart', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'ticket',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='travelplan_geo',
            fields=[
                ('travelplan_geo_id', models.AutoField(primary_key=True, serialize=False)),
                ('gpxtrek', models.TextField(null=True)),
                ('graph_data', models.JSONField(blank=True, null=True)),
                ('geojson', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='traveltype',
            fields=[
                ('traveltype_id', models.AutoField(primary_key=True, serialize=False)),
                ('traveltypedescription', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'traveltype',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='typeexpense',
            fields=[
                ('typeexpense_id', models.AutoField(primary_key=True, serialize=False)),
                ('nametypeexpense', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'typeexpense',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='travelplan',
            fields=[
                ('travelplan_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=50)),
                ('territory', models.CharField(max_length=100)),
                ('datestart', models.DateTimeField()),
                ('datefinish', models.DateTimeField()),
                ('quantitydays', models.IntegerField()),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('friends_only', models.BooleanField(default=False)),
                ('total_distance_travelled', models.FloatField(blank=True, null=True)),
                ('total_time_seconds', models.IntegerField(blank=True, null=True)),
                ('moving_time_seconds', models.IntegerField(blank=True, null=True)),
                ('speed_midle', models.FloatField(blank=True, null=True)),
                ('speed_moving', models.FloatField(blank=True, null=True)),
                ('total_ascent', models.FloatField(blank=True, null=True)),
                ('total_descent', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(max_length=30)),
                ('travelplan_geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan_geo')),
                ('traveltype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.traveltype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'travelplan',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='expense',
            fields=[
                ('expense_id', models.AutoField(primary_key=True, serialize=False)),
                ('nameexpense', models.CharField(max_length=70)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity_day', models.IntegerField()),
                ('quantity_people', models.IntegerField()),
                ('full_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('typeexpense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='travel.typeexpense')),
            ],
            options={
                'db_table': 'expense',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='travelplanticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.ticket')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'ticket')},
            },
        ),
        migrations.CreateModel(
            name='travelplansight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.sight')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'sight')},
            },
        ),
        migrations.CreateModel(
            name='travelplanexpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.expense')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'expense')},
            },
        ),
        migrations.CreateModel(
            name='travelplandescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.description')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'description')},
            },
        ),
        migrations.CreateModel(
            name='travelplanbooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.booking')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'booking')},
            },
        ),
        migrations.CreateModel(
            name='plpoint_trek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_trek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.point_trek')),
                ('travelplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.travelplan')),
            ],
            options={
                'unique_together': {('travelplan', 'point_trek')},
            },
        ),
    ]
