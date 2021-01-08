import hmac
from tool.authorization_token import *
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import pagination
from rest_framework import permissions
from tool.serializer import my_serializer
from WEBAPI.models import *


class MyFilter(filters.BaseFilterBackend):
    """
    自定义搜索类
    """

    def filter_queryset(self, request, queryset, view):
        """
        自定义搜索
        :param request:
        :param queryset:
        :param view:
        :return:
        """
        print("我是自定义过滤器")
        return queryset


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


class Operator(ListAPIView, CreateAPIView, UpdateAPIView):
    """
    标注员相关
    """
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # 可查询字段
    search_fields = ()
    # 允许排序字段
    # ordering_fields = ("creator",)
    ordering_fields = "__all__"
    pagination_class = pagination.LimitOffsetPagination

    # TODO
    permissions_classes = (permissions.AllowAny, permissions.IsAuthenticated)

    # 重写分页后的返回数据json样式
    def get_paginated_response(self, data):
        print(self.paginator)
        return Response({
            "code": 0,
            'next': self.paginator.get_next_link(),
            'previous': self.paginator.get_previous_link(),
            "data": data
        })

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
        # if identity == "admin":

        # 子序列化器，用来对外键数据进行规范
        operator_serializer = my_serializer(WangtoOperator, field=("state", "register_time", "nick_name", "id"),
                                            is_child=True)

        # 查询 (filter_queryset参数必须是查询结果集)
        my_operator = self.filter_queryset(user_obj.my_leader.all())

        # 分页
        page = self.paginate_queryset(my_operator)
        if page is not None:
            serializer = my_serializer(WangtoUser, page, True,
                                       field=["nick_name", "state", "register_time", "identity", "creator"],
                                       childs={"WangtoOperator": operator_serializer})
            return self.get_paginated_response(serializer.data)

        serializer = my_serializer(WangtoUser, my_operator, True,
                                   field=["nick_name", "register_time", "identity", "creator"],
                                   childs={"WangtoOperator": operator_serializer})

        return Response(serializer.data)

    @check_bg_authorization_token
    def create(self, request, *args, **kwargs):
        print(123)
        # serializer = self.get_serializer(data=request.data)
        serializer = my_serializer(WangtoOperator, data={"nick_name": "hahaha"})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @check_bg_authorization_token
    def update(self, request, *args, **kwargs):

        instance = WangtoOperator.objects.get(id=1)
        serializer = my_serializer(WangtoOperator, instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
