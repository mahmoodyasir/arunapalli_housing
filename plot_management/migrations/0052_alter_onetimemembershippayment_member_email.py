# Generated by Django 4.0.5 on 2022-07-12 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0051_onetimemembershippayment_bank_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimemembershippayment',
            name='member_email',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
