# Generated by Django 4.0.5 on 2022-06-24 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0043_trackmembershippayment_online_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackmembershippayment',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trackmembershippayment',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
