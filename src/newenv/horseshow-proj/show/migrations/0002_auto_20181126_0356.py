# Generated by Django 2.1 on 2018-11-26 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horseridercombo',
            name='num',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
