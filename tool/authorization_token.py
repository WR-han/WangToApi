from WEBAPI.models import WangtoUser
from rest_framework import response
from key.key import *

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

    def decorator(self, request, *args, **kwargs):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
            res = jwt.decode(token.encode(), salt, algorithms="HS256")
            wangto_user_id = res["wangto_user_id"]
            wangto_user_obj = WangtoUser.objects.get(id=wangto_user_id)
            setattr(request, "user_obj", wangto_user_obj)
            setattr(request, "identity", wangto_user_obj.identity)

        except Exception as e:
            return response.Response({
                "code": 401,
                "data": "验证失败",
                "msg": f"{e}"
            })

        return func(self, request, *args, **kwargs)

    return decorator
