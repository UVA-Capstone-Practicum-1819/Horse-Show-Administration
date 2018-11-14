# Generated by Django 2.1 on 2018-11-13 22:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(default='', max_length=100)),
                ('class_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_name', models.CharField(default='', max_length=100)),
                ('division_number', models.IntegerField(default=0)),
                ('classes', models.ManyToManyField(blank=True, null=True, to='show.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Horse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('barn_name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('coggins', models.IntegerField()),
                ('owner', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HorseRiderCombo',
            fields=[
                ('num', models.IntegerField(default=-1, primary_key=True, serialize=False)),
                ('horse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Horse')),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('email', models.EmailField(max_length=200, validators=[django.core.validators.EmailValidator()])),
                ('horses', models.ManyToManyField(through='show.HorseRiderCombo', to='show.Horse')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_name', models.CharField(max_length=100)),
                ('show_date', models.CharField(max_length=100)),
                ('show_location', models.CharField(max_length=100)),
                ('show_divisions', models.ManyToManyField(blank=True, null=True, to='show.Division')),
            ],
        ),
        migrations.AddField(
            model_name='horseridercombo',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Rider'),
        ),
    ]
