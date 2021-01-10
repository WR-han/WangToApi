from tool.authorization_token import *
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from tool.my_serializer import my_serializer
from tool.my_serializer import MyPagination
from WEBAPI.models import *


class Operator(ListAPIView, CreateAPIView, UpdateAPIView):
    """
    标注员相关
    """
    # 可查询字段默认值
    search_fields = ()
    # 可排序字段
    ordering_fields = "__all__"
    # 分页模板
    pagination_class = MyPagination

    @check_bg_authorization_token
    def list(self, request, *args, **kwargs):

        # 权限
        identity = request.identity
        # 用户实例
        user_obj = request.user_obj
        # 前端搜索字段
        self.search_fields = request.search_fields
        # 请求分类
        data_category = request.data_category
        print(data_category)
        # 判断权限
        if identity == "admin":
            # 需要序列化的查询结果集
            # queryset = user_obj.my_leader.all()
            queryset = WangtoOperator.objects.filter(owner=user_obj)
            # 筛选后的查询结果集_queryset参数必须是查询结果集)
            screen_queryset = self.filter_queryset(queryset)
            # 子序列化器，用来对外键数据进行规范
            creator_serializer = my_serializer(WangtoUser, field=("nick_name",), is_child=True)
            # 分页后的查询结果集
            page = self.paginate_queryset(screen_queryset)
            # 设定序列化条件
            # print(getattr(WangtoOperator, "nick_name").field.verbose_name)
            serializer = my_serializer(WangtoOperator, many=True,
                                       field=["id", "nick_name", "account", "register_time", "expire_time", "state"],
                                       childs={"creator": (creator_serializer, False)})
            # 存在分页查询
            if page is not None:
                serializer.instance = page
                return self.get_paginated_response(serializer)
            return Response({
                "code": 403,
                "data": "必须携带分页数量参数"
            })

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


class Leader(ListAPIView, CreateAPIView, UpdateAPIView):
    """
    管理员相关
    """
    # 可查询字段默认值
    search_fields = ()
    # 可排序字段
    ordering_fields = "__all__"
    # 分页模板
    pagination_class = MyPagination

    @check_bg_authorization_token
    def list(self, request, *args, **kwargs):

        # 权限
        identity = request.identity
        # 用户实例
        user_obj = request.user_obj
        # 前端搜索字段
        self.search_fields = request.search_fields
        # 判断权限
        if identity == "admin":
            # 需要序列化的查询结果集
            # queryset = user_obj.my_leader.all()
            queryset = WangtoOperator.objects.filter(owner=user_obj)
            # 筛选后的查询结果集_queryset参数必须是查询结果集)
            screen_queryset = self.filter_queryset(queryset)
            # 子序列化器，用来对外键数据进行规范
            creator_serializer = my_serializer(WangtoUser, field=("nick_name",), is_child=True)
            # 分页后的查询结果集
            page = self.paginate_queryset(screen_queryset)
            # 设定序列化条件
            # print(getattr(WangtoOperator, "nick_name").field.verbose_name)
            serializer = my_serializer(WangtoOperator, many=True,
                                       field=["id", "nick_name", "account", "register_time", "expire_time", "state"],
                                       childs={"creator": (creator_serializer, False)})
            # 存在分页查询
            if page is not None:
                serializer.instance = page
                return self.get_paginated_response(serializer)
            return Response({
                "code": 403,
                "data": "必须携带分页数量参数"
            })
