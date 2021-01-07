# Generated by Django 3.1.4 on 2021-01-06 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WEBAPI', '0006_auto_20210106_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wangtouser',
            name='team',
        ),
        migrations.AddField(
            model_name='wangtoteam',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='WangtoTeam', to='WEBAPI.wangtouser', verbose_name='负责人'),
        ),
        migrations.AlterField(
            model_name='wangtoteam',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_team', to='WEBAPI.wangtouser', verbose_name='创建者'),
        ),
        migrations.DeleteModel(
            name='WangtoTeamAllocation',
        ),
    ]