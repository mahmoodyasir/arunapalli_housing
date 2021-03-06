# Generated by Django 4.0.5 on 2022-06-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0045_memberhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberhistory',
            name='member_firstname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='memberhistory',
            name='member_lastname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='memberhistory',
            name='member_nid',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='memberhistory',
            name='member_phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
