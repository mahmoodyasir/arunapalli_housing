# Generated by Django 4.0.5 on 2022-06-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0005_onetimemembershippayment_member_onetime_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_nid',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
