from django.db import models


# Create your models here.


class WangtoPaymentRecords(models.Model):
    """
    缴费记录表
    """
    owner = models.ForeignKey("WangtoUser", on_delete=models.CASCADE, related_name="WangtoPaymentRecords",
                              verbose_name="所有者")
