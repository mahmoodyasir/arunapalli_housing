# Generated by Django 4.0.5 on 2022-06-21 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0039_alter_trackmembershippayment_member_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackmembershippayment',
            name='offline_payment_id',
        ),
    ]