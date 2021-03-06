# Generated by Django 3.1.4 on 2021-01-13 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wangtoinspector',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='WangtoInspector', to='WEBAPI.wangtouser', verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='wangtooperator',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='WangtoOperator', to='WEBAPI.wangtouser', verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='wangtouser',
            name='identity',
            field=models.CharField(choices=[('admin', '管理员'), ('leader', '项目负责人')], max_length=6, verbose_name='身份'),
        ),
    ]
