# Generated by Django 4.0.5 on 2022-06-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0027_offlinepayment_end_date_offlinepayment_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackmembershippayment',
            name='payment_type',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
