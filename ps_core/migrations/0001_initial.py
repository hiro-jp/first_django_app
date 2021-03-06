# Generated by Django 2.2.1 on 2019-05-22 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('date_ent', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SkillMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ps_core.Rank')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ps_core.Skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ps_core.Person')),
            ],
        ),
        migrations.CreateModel(
            name='RefRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ps_core.Rank')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ps_core.Skill')),
            ],
        ),
    ]
