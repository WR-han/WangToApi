# Generated by Django 3.1.4 on 2021-01-05 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPI', '0002_auto_20210105_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wangtoinspector',
            old_name='passworld',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='wangtooperator',
            old_name='passworld',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='wangtouser',
            old_name='passworld',
            new_name='password',
        ),
        migrations.AlterField(
            model_name='wangtodata',
            name='state',
            field=models.CharField(choices=[('invalid', '弃用'), ('active', '激活')], max_length=7, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='wangtodataset',
            name='state',
            field=models.CharField(choices=[('invalid', '弃用'), ('active', '激活')], max_length=7, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='wangtoinspector',
            name='state',
            field=models.CharField(choices=[('invalid', '弃用'), ('active', '激活')], max_length=7, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='wangtooperator',
            name='state',
            field=models.CharField(choices=[('invalid', '弃用'), ('active', '激活')], max_length=7, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='wangtouser',
            name='identity',
            field=models.CharField(choices=[('admin', '管理员'), ('leader', '项目负责人')], max_length=6, verbose_name='身份'),
        ),
        migrations.AlterField(
            model_name='wangtouser',
            name='state',
            field=models.CharField(choices=[('invalid', '弃用'), ('active', '激活')], max_length=7, verbose_name='状态'),
        ),
    ]
