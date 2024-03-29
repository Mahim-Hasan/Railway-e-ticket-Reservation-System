# Generated by Django 3.0.7 on 2021-03-30 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Start',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_no', models.CharField(max_length=20)),
                ('start', models.CharField(max_length=20)),
                ('end', models.CharField(max_length=20)),
                ('total_seats', models.IntegerField()),
                ('class_type', models.CharField(max_length=20)),
                ('cost', models.IntegerField()),
                ('travel_time', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Train')),
            ],
        ),
        migrations.CreateModel(
            name='End',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('distance', models.FloatField()),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Start')),
                ('train', models.ManyToManyField(to='main.Train')),
            ],
        ),
    ]
