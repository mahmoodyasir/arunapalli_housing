# Generated by Django 4.0.5 on 2022-06-24 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0042_payonline_medium_payonline_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackmembershippayment',
            name='online_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plot_management.payonline'),
        ),
    ]
