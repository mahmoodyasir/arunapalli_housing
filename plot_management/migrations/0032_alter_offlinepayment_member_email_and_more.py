# Generated by Django 4.0.5 on 2022-06-19 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0031_alter_offlinepayment_member_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offlinepayment',
            name='member_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plot_management.member'),
        ),
        migrations.AlterField(
            model_name='offlinepayment',
            name='member_status',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='plot_management.status'),
        ),
    ]