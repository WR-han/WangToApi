from django.db import models


# Create your models here.


class WangtoProject(models.Model):
    """
    项目表
    """
    project_name = models.CharField("项目名称", max_length=30)


class WangtoDataStet(models.Model):
    """
    数据集表
    """
    pass


class WangtoData(models.Model):
    """
    数据表
    """
    pass
