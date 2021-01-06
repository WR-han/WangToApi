import hmac

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListAPIView

from tool.authorization_token import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import pagination
from tool.serializer import my_serializer
from WEBAPI.models import *


class Account(APIView):
    """
    账户相关
    """

    @check_bg_authorization_token
    def get(self, request):
        """
        获取账户相关信息
        """
        pass

    def post(self, request):
        """
        账号登陆
        """
        # json格式检查
        try:
            password = request.data["password"]
            account = request.data["account"]
        except Exception as e:
            return response.Response({
                "code": 404,
                "data": "json参数有误",
                "msg": f"{e}"
            })

        # 数据库查询
        try:
            account_obj = WangtoUser.objects.get(account=account)
            if password == account:
                password_h = password
            else:
                h = hmac.new(salt, password.encode(), digestmod="sha256")
                password_h = h.hexdigest()

            # 密码比对
            if account_obj.password == password_h:
                # 生成token
                token = make_bg_authorization_token(wangto_user_id=account_obj.pk)
                return response.Response({
                    "code": 200,
                    "data": {"token": token}
                })

            else:
                return response.Response({
                    "code": 401,
                    "data": "密码错误"
                })

        except Exception as e:
            return response.Response({
                "code": 401,
                "data": "用户不存在",
                "msg": f"{e}"
            })

    @check_bg_authorization_token
    def put(self, request):
        pass


class Operator(ListAPIView):
    """
    标注员相关
    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ()
    pagination_class = pagination.LimitOffsetPagination

    # 重写分页后的返回数据json样式
    def get_paginated_response(self, data):
        print(self.paginator)
        return Response({
            "code": 0,
            'next': self.paginator.get_next_link(),
            'previous': self.paginator.get_previous_link(),
            "data": data
        })

        # return self.paginator.get_paginated_response(data)

    @check_bg_authorization_token
    def list(self, request, *args, **kwargs):
        # 权限
        identity = request.identity
        # 用户实例
        user_obj = request.user_obj

        # 前端搜索字段
        try:
            search_field = request.GET["field"]
            self.search_fields = (search_field,)
        except MultiValueDictKeyError as e:
            self.search_fields = ()

        # 判断权限
        if identity == "admin":
            my_operator = self.filter_queryset(user_obj.my_operator.order_by("creator"))

            # 分页
            page = self.paginate_queryset(my_operator)
            if page is not None:
                serializer = my_serializer(WangtoOperator, page, True,
                                           field=("nick_name", "state", "register_time", "expire_time", "creator"))
                return self.get_paginated_response(serializer.data)

            serializer = my_serializer(WangtoOperator, my_operator, True,
                                       field=("nick_name", "state", "register_time", "expire_time", "creator"))

            return Response(serializer.data)
