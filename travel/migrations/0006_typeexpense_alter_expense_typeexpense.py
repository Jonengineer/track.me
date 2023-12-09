# Generated by Django 4.2.6 on 2023-12-08 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_expense_nameexpense'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='expense',
            name='typeexpense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='travel.typeexpense'),
        ),
    ]
