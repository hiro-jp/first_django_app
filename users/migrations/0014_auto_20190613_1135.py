# Generated by Django 2.2.1 on 2019-06-13 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_is_approver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='manager',
            field=models.ForeignKey(blank=True, help_text='各組織単位にひとりのリーダー。グループならGM、チームならTL。彼らはグループ員の情報を閲覧できる。承認権限はUserクラスのapproverが受け持つ。', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_approver',
            field=models.BooleanField(default=False, help_text='承認権限。GMには承認権限があり、TLに承認権限がない場合、承認権限と閲覧権限を分ける。ふつう、approverのほうが、Unitのmanagerより少ない。', verbose_name='approver'),
        ),
    ]
