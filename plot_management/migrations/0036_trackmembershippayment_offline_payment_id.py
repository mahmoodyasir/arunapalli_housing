# Generated by Django 4.0.5 on 2022-06-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0035_trackmembershippayment_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackmembershippayment',
            name='offline_payment_id',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
