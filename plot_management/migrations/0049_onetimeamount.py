# Generated by Django 4.0.5 on 2022-07-09 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0048_alter_onetimemembershippayment_member_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnetimeAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
