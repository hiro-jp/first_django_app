# Generated by Django 2.2.1 on 2019-06-29 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ps_core', '0019_auto_20190629_0224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skillgroup',
            name='skill_set',
        ),
        migrations.AddField(
            model_name='skill',
            name='skill_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ps_core.SkillGroup'),
        ),
    ]
