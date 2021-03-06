# Generated by Django 4.0.5 on 2022-06-24 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0040_remove_trackmembershippayment_offline_payment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayOnline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_nid', models.CharField(blank=True, max_length=200, null=True)),
                ('plot_no', models.CharField(blank=True, max_length=199, null=True)),
                ('road_no', models.CharField(blank=True, max_length=199, null=True)),
                ('paid_amount', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plot_management.member')),
                ('member_status', models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='plot_management.status')),
            ],
        ),
    ]
