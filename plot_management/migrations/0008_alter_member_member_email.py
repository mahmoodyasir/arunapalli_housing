# Generated by Django 4.0.5 on 2022-06-14 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0007_alter_member_member_firstname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]