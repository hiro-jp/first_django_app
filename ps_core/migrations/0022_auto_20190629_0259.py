# Generated by Django 2.2.1 on 2019-06-29 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_core', '0021_auto_20190629_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillgroup',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
