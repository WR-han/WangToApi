from WEBAPI.models import WangtoUser
from rest_framework import response
from key.key import *
from functools import wraps
from django.utils.datastructures import MultiValueDictKeyError

import datetime
import jwt


def make_bg_authorization_token(wangto_user_id, expire_hour=expire):
    """
    token生成器
    :param wangto_user_id: 用户id
    :param expire_hour: 过期时间(小时)
    :return:
    """

    playload = {
        "wangto_user_id": wangto_user_id,
        "iss": "WangTo",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expire_hour),
        "iat": datetime.datetime.utcnow(),
    }

    signature = jwt.encode(playload, salt, algorithm="HS256")

    return signature


def check_bg_authorization_token(func):
    """
    token验证装饰器 进行token验证,并将token中用户对应的user_obj加入request中
    :param func: 请求函数(get/post/put/delete......)
    :return:
    """

    @wraps(func)
    def decorator(self, request, *args, **kwargs):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
            res = jwt.decode(token.encode(), salt, algorithms="HS256")
            wangto_user_id = res["wangto_user_id"]
            wangto_user_obj = WangtoUser.objects.get(id=wangto_user_id)
            # 前端搜索字段
            try:
                search_fields = request.GET["field"].split(",")
            except MultiValueDictKeyError as e:
                search_fields = ()
            try:
                data_category = request.GET["data_category"]
            except MultiValueDictKeyError as e:
                data_category = None
            setattr(request, "user_obj", wangto_user_obj)
            setattr(request, "identity", wangto_user_obj.identity)
            setattr(request, "search_fields", search_fields)
            setattr(request, "data_category", data_category)

        except Exception as e:
            return response.Response({
                "code": 401,
                "data": "验证失败",
                "msg": f"{e}"
            })

        return func(self, request, *args, **kwargs)

    return decorator
