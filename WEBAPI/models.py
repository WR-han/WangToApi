from django.db import models


# Create your models here.

class WangtoAdmin(models.Model):
    """
    wangto管理员账户表
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
    account = models.OneToOneField("WangtoAccount", on_delete=models.CASCADE, null=True, blank=True)
    information = models.OneToOneField("WangtoUserInfo", on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField("状态", max_length=7, choices=state_choices)
    identity = models.CharField("身份", max_length=6, choices=identity_choices)
    register_time = models.DateTimeField("注册时间", auto_now_add=True)


class WangtoAccount(models.Model):
    # owner = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, related_name="my_cost_bill", verbose_name="所有者")
    due_date = models.DateTimeField("存储有效期", auto_now_add=True)
    capacity = models.BigIntegerField("储存容量", default=0)
    data_size = models.BigIntegerField("现有数据大小", default=0)


class WangtoUserInfo(models.Model):
    company = models.CharField("公司名称", max_length=50, null=True, blank=True)


class WangtoProject(models.Model):
    project_name = models.CharField("项目名称", max_length=30)


class WangtoDataStet(models.Model):
    pass


class WangtoData(models.Model):
    pass


class WangtoInspector(models.Model):
    pass


class WangtoOperator(models.Model):
    pass


class WangtoRechargeBill(models.Model):
    owner = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, related_name="my_recharge_bill",
                              verbose_name="所有者")
