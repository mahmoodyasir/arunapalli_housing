# Generated by Django 4.0.5 on 2022-07-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0050_bankname'),
    ]

    operations = [
        migrations.AddField(
            model_name='onetimemembershippayment',
            name='bank_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]