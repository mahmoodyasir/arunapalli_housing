# Generated by Django 4.0.5 on 2022-06-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0037_alter_trackmembershippayment_member_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackmembershippayment',
            name='member_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]