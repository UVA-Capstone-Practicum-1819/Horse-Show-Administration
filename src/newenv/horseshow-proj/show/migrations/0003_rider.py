# Generated by Django 2.1.2 on 2018-10-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0002_horse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
            ],
        ),
    ]
