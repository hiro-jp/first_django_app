# Generated by Django 2.2.1 on 2019-06-02 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ps_core', '0015_auto_20190601_1233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='updaterequest',
            options={'permissions': (('can_create', 'Can create update request'), ('can_approve', 'Can approve update request'))},
        ),
    ]
