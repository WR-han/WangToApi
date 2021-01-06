import hmac

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListAPIView

from tool.authorization_token import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
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

        # 分页
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        if identity == "admin":
            operator_qs = None

            for leader in user_obj.my_leader.all():
                if not operator_qs:
                    operator_qs = leader.WangtoOperator.all()
                else:
                    operator_qs += leader.WangtoOperator.all()
                # queryset = self.filter_queryset(leader.WangtoOperator.all())
                # leader_operator = my_serializer(WangtoOperator, queryset, True,
                #                                 field=("nick_name", "state", "register_time", "expire_time"),
                #                                 _depth=1).data
                # operator_dict[leader.account] = leader_operator

            operator_qs = self.filter_queryset(operator_qs)
            leader_operator = my_serializer(WangtoOperator, operator_qs, True,
                                            field=("nick_name", "state", "register_time", "expire_time"),
                                            _depth=1).data

            # print(operator_qs)
            return Response(leader_operator)

        # serializer = my_serializer(WangtoUser, queryset, field=("WangtoOperator",), many=True, _depth=1)
        # return Response(serializer.data)

    # class Operator(APIView):
#     """
#     标注员相关
#     """
#
#     @check_bg_authorization_token
#     def get(self, request):
#         # 权限
#         identity = request.identity
#         # 用户实例
#         user_obj = request.user_obj
#
#         # print(WangtoUser)
#
#         # 管理员
#         if identity == "admin":
#
#             operator_dict = {}
#
#             my_operator = my_serializer(WangtoUser, user_obj, False, field=("WangtoOperator",), _depth=1).data["WangtoOperator"]
#             operator_dict["my"] = my_operator
#
#             for leader in user_obj.my_leader.all():
#                 leader_operator = my_serializer(WangtoUser, leader, False, field=("WangtoOperator",), _depth=1).data["WangtoOperator"]
#                 operator_dict[leader.account] = leader_operator
#
#             # serializer = my_serializer(WangtoUser, user_obj, False, field=("my_leader",),_depth=1)
#
#             return Response(operator_dict)
