# Generated by Django 4.0.5 on 2022-06-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=199)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
