# Generated by Django 2.2.1 on 2019-05-30 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ps_core', '0008_auto_20190530_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updaterequest',
            name='status',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
