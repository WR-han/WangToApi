# Generated by Django 2.2.2 on 2021-01-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPI', '0004_auto_20210106_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='wangtoinspector',
            name='nick_name',
            field=models.CharField(default='wangto审核员', max_length=20, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='wangtooperator',
            name='nick_name',
            field=models.CharField(default='wangto标注员', max_length=20, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='wangtouser',
            name='nick_name',
            field=models.CharField(default='wangto用户', max_length=20, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='wangtouser',
            name='identity',
            field=models.CharField(choices=[('admin', '管理员'), ('leader', '项目负责人')], max_length=6, verbose_name='身份'),
        ),
    ]
