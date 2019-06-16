# Generated by Django 2.2.1 on 2019-06-14 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=20)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('phone', models.CharField(blank=True, max_length=40)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
    ]
