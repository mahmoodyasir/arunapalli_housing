# Generated by Django 4.0.5 on 2022-06-16 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plot_management', '0015_alter_member_default_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='member_email',
            new_name='prouser',
        ),
        migrations.RemoveField(
            model_name='member',
            name='default_email',
        ),
    ]
