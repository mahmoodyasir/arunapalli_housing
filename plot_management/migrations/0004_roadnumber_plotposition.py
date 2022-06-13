# Generated by Django 4.0.5 on 2022-06-13 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0003_paymentstatus_offlinepayment_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlotPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_no', models.CharField(max_length=199, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('road_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plot_management.roadnumber')),
            ],
        ),
    ]
