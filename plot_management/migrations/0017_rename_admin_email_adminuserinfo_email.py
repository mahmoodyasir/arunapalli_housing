# Generated by Django 4.0.5 on 2022-06-16 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0016_rename_member_email_member_prouser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminuserinfo',
            old_name='admin_email',
            new_name='email',
        ),
    ]
