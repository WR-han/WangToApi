from django.dispatch import receiver
from django.db.models.signals import post_save

from WEBAPI import models


@receiver(post_save, sender=models.WangtoDataSetAllocation)
def create_data_allocation(**kwargs):
    print("接收信号")
    data_set_allocation = kwargs["instance"]

    print(data_set_allocation.data_set.WangtoDate.all())
    pass
