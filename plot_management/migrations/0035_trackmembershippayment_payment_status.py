# Generated by Django 4.0.5 on 2022-06-21 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0034_paymentdatefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackmembershippayment',
            name='payment_status',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
