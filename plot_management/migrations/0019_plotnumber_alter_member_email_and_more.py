# Generated by Django 4.0.5 on 2022-06-16 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0018_rename_email_adminuserinfo_admin_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlotNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='plotposition',
            name='plot_no',
            field=models.CharField(blank=True, max_length=199, null=True),
        ),
        migrations.AlterField(
            model_name='plotposition',
            name='road_no',
            field=models.CharField(blank=True, max_length=199, null=True),
        ),
        migrations.AlterField(
            model_name='roadnumber',
            name='title',
            field=models.CharField(max_length=155, unique=True),
        ),
    ]
