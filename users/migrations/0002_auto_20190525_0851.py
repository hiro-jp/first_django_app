# Generated by Django 2.2.1 on 2019-05-25 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='employee_code',
            field=models.CharField(default=0, help_text='Required 7 digit code.', max_length=7, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d\\d\\d\\d\\d\\d\\d$')]),
            preserve_default=False,
        ),
    ]
