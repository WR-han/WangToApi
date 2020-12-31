from django.db import models


# Create your models here.

class WangtoUser(models.Model):
    """
    后台用户基础数据表
    """
    state_choices = {
        ("active", "激活"),
        ("invalid", "弃用")
    }
    identity_choices = {
        ("admin", "管理员"),
        ("leader", "项目负责人")
    }
    # OSSID = models.CharField("OSSID", max_length=16)
    mobile = models.CharField("手机号/登录账号", max_length=11)
    passworld = models.CharField("密码", max_length=64)
    account = models.OneToOneField("WangtoAccount", on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="账户数据")
    information = models.OneToOneField("WangtoUserInfo", on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="其他信息")
    state = models.CharField("状态", max_length=7, choices=state_choices)
    identity = models.CharField("身份", max_length=6, choices=identity_choices)
    register_time = models.DateTimeField("注册时间", auto_now_add=True)
    creator = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="创建者")
    team = models.ManyToManyField("WangtoTeam", verbose_name='相关团队', through='WangtoU2T', related_name='WangtoUser')


class WangtoAccount(models.Model):
    """
    后台用户账户数据表
    """
    # owner = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, related_name="my_cost_bill", verbose_name="所有者")
    due_date = models.DateTimeField("存储有效期", auto_now_add=True)
    capacity = models.BigIntegerField("储存容量", default=0)
    data_size = models.BigIntegerField("现有数据大小", default=0)


class WangtoUserInfo(models.Model):
    """
    后台用户其他信息表
    """
    company = models.CharField("公司名称", max_length=50, null=True, blank=True)


class WangtoU2T(models.Model):
    """
    用户<->团队中间表
    """
    # WangtoUser = models.ForeignKey("")
    pass


class WangtoTeam(models.Model):
    """
    团队数据表
    """
    pass


class WangtoInspector(models.Model):
    """
    审核员表
    """

    pass


class WangtoOperator(models.Model):
    """
    标注员表
    """
    pass
