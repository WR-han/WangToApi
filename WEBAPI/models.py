from django.db import models


# ▼ --------------------------------------- ▼  user_models  ▼ --------------------------------------- ▼
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

    nick_name = models.CharField("昵称", max_length=20, default="wangto用户")
    account = models.CharField("手机号/登录账号", max_length=11)
    password = models.CharField("密码", max_length=64)
    account_msg = models.OneToOneField("WangtoAccount", on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="账户数据")
    information = models.OneToOneField("WangtoUserInfo", on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="其他信息")

    creator = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="my_leader",
                                verbose_name="创建者")
    team = models.ManyToManyField("WangtoTeam", verbose_name="相关团队", through="WangtoTeamAllocation",
                                  related_name="WangtoUser")

    state = models.CharField("状态", max_length=7, choices=state_choices)
    identity = models.CharField("身份", max_length=6, choices=identity_choices)

    register_time = models.DateTimeField("注册时间", auto_now_add=True)

    def __str__(self):
        return '用户-{}'.format(self.nick_name)


class WangtoAccount(models.Model):
    """
    后台用户账户数据表
    """
    due_date = models.DateTimeField("存储有效期", auto_now_add=True)
    capacity = models.BigIntegerField("储存容量", default=0)
    now_data_size = models.BigIntegerField("现有总数据大小", default=0)
    data_money = models.PositiveIntegerField("剩余流量金额", default=0)


class WangtoUserInfo(models.Model):
    """
    后台用户其他信息表
    """
    company = models.CharField("公司名称", max_length=30, null=True, blank=True)


class WangtoTeamAllocation(models.Model):
    """
    团队分配表
    用户(项目负责人)<->团队 中间表
    """
    WangtoUser = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, verbose_name="用户",
                                   related_name="WangtoTeamAllocation")
    WangtoTeam = models.ForeignKey("WangtoTeam", on_delete=models.CASCADE, verbose_name="团队",
                                   related_name="WangtoTeamAllocation")

    allocation_time = models.DateTimeField("分配时间", auto_now_add=True)


class WangtoTeam(models.Model):
    """
    团队表
    """
    team_name = models.CharField("团队名称", max_length=20)

    creator = models.ForeignKey("WangtoUser", on_delete=models.SET_NULL, verbose_name="创建者", related_name="WangtoTeam",
                                null=True, blank=True)

    register_time = models.DateTimeField("注册时间", auto_now_add=True)


class WangtoInspector(models.Model):
    """
    审核员表
    """
    state_choices = {
        ("active", "激活"),
        ("invalid", "弃用")
    }

    nick_name = models.CharField("昵称", max_length=20, default="wangto审核员")
    account = models.CharField("手机号/登录账号", max_length=11)
    password = models.CharField("密码", max_length=64)

    creator = models.ForeignKey("WangtoUser", on_delete=models.SET_NULL, verbose_name="创建者",
                                related_name="WangtoInspector", null=True, blank=True)
    data = models.ManyToManyField("WangtoData", verbose_name="分配任务", through="WangtoDataAllocation",
                                  related_name="WangtoInspector")

    state = models.CharField("状态", max_length=7, choices=state_choices)

    register_time = models.DateTimeField("注册时间", auto_now_add=True)
    expire_time = models.DateTimeField("到期时间", null=True, blank=True)

    def __str__(self):
        return '审核员-{}'.format(self.nick_name)


class WangtoOperator(models.Model):
    """
    标注员表
    """
    state_choices = {
        ("active", "激活"),
        ("invalid", "弃用")
    }

    nick_name = models.CharField("昵称", max_length=20, default="wangto标注员")
    account = models.CharField("手机号/登录账号", max_length=11)
    password = models.CharField("密码", max_length=64)

    creator = models.ForeignKey("WangtoUser", on_delete=models.SET_NULL, verbose_name="创建者",
                                related_name="WangtoOperator", null=True, blank=True)
    data = models.ManyToManyField("WangtoData", verbose_name="分配任务", through="WangtoDataAllocation",
                                  related_name="WangtoOperator")

    state = models.CharField("状态", max_length=7, choices=state_choices)

    register_time = models.DateTimeField("注册时间", auto_now_add=True)
    expire_time = models.DateTimeField("到期时间", null=True, blank=True)

    def __str__(self):
        return '标注员-{}'.format(self.nick_name)


# ▼ --------------------------------------- ▼  data_models  ▼ --------------------------------------- ▼
class WangtoProject(models.Model):
    """
    项目表
    """
    project_name = models.CharField("项目名称", max_length=30)

    data = models.ManyToManyField("WangtoData", verbose_name="所用数据", through="WangtoDataAllocation",
                                  related_name="WangtoProject")
    data_set = models.ManyToManyField("WangtoDataSet", verbose_name="所用数据集", through="WangtoDataSetAllocation",
                                      related_name="WangtoProject")

    start_time = models.DateTimeField("开始时间", auto_now_add=True)
    end_time = models.DateTimeField("结束时间", null=True, blank=True)


class WangtoDataSetAllocation(models.Model):
    """
    数据集分配表
    数据集<->项目 中间表
    """
    project = models.ForeignKey("WangtoProject", on_delete=models.CASCADE, verbose_name="项目",
                                related_name="WangtoDataSetAllocation", null=True, blank=True)
    data_set = models.ForeignKey("WangtoDataSet", on_delete=models.CASCADE, verbose_name="数据集名",
                                 related_name="WangtoDataSetAllocation", null=True, blank=True)


class WangtoDataSet(models.Model):
    """
    数据集表
    """
    state_choices = {
        ("active", "激活"),
        ("invalid", "弃用")
    }

    data_set_name = models.CharField("数据集名称", max_length=30)
    data_num = models.PositiveIntegerField("数据量", default=0)

    state = models.CharField("状态", max_length=7, choices=state_choices)

    create_time = models.DateTimeField("上传时间", auto_now_add=True)


class WangtoData(models.Model):
    """
    数据表
    """
    state_choices = {
        ("active", "激活"),
        ("invalid", "弃用")
    }

    data_name = models.CharField("数据名称", max_length=30)
    data_size = models.PositiveIntegerField("文件大小", default=0)

    data_set = models.ForeignKey("WangtoDataSet", on_delete=models.CASCADE, verbose_name="所属数据集",
                                 related_name="WangtoDate")

    state = models.CharField("状态", max_length=7, choices=state_choices)

    upload_time = models.DateTimeField("上传时间", auto_now_add=True)


# ▼ --------------------------------------- ▼  statistical_models  ▼ --------------------------------------- ▼
class WangtoPaymentRecords(models.Model):
    """
    缴费记录表
    """
    owner = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, related_name="WangtoPaymentRecords",
                              verbose_name="所有者")


class WangtoDataAllocation(models.Model):
    """
    数据分配表/数据统计
    数据<->标注员 中间表
    """
    project = models.ForeignKey("WangtoProject", on_delete=models.CASCADE, verbose_name="项目",
                                related_name="WangtoDataAllocation")
    data = models.ForeignKey("WangtoData", on_delete=models.CASCADE, verbose_name="数据名",
                             related_name="WangtoDataAllocation")
    inspector = models.ForeignKey("WangtoInspector", on_delete=models.CASCADE, verbose_name="审核员",
                                  related_name="WangtoDataAllocation")
    operator = models.ForeignKey("WangtoOperator", on_delete=models.CASCADE, verbose_name="标注员",
                                 related_name="WangtoDataAllocation")

    is_inspect = models.BooleanField("是否审核", default=False)
    is_operate = models.BooleanField("是否标注", default=False)
    data_size = models.PositiveIntegerField("文件大小", default=0)

    inspect_time = models.DateTimeField("审核时间", null=True, blank=True)
    operate_time = models.DateTimeField("标注时间", null=True, blank=True)
