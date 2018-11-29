# Generated by Django 2.1 on 2018-11-26 06:14

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
                ('name', models.CharField(default='', max_length=100)),
                ('number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('number', models.IntegerField(default=0)),
                ('classes', models.ManyToManyField(to='show.Classes')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('horse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Horse')),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('email', models.EmailField(max_length=200, primary_key=True, serialize=False, validators=[django.core.validators.EmailValidator()])),
                ('horses', models.ManyToManyField(through='show.HorseRiderCombo', to='show.Horse')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('dayOfPrice', models.IntegerField(blank=True, null=True)),
                ('preRegistrationPrice', models.IntegerField(blank=True, null=True)),
                ('divisions', models.ManyToManyField(blank=True, to='show.Division')),
            ],
        ),
        migrations.AddField(
            model_name='horseridercombo',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Rider'),
        ),
    ]
