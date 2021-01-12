import datetime as sb

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from WEBAPI.models import *
from tool.authorization_token import *
from tool.my_serializer import my_serializer
from tool.others import MyPagination


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
        # 请求数据类型
        data_category = request.data_category
        # 判断权限
        if identity == "admin":
            # 需要序列化的查询结果集
            queryset = WangtoOperator.objects.filter(owner=user_obj)
            # 筛选后的查询结果集_queryset参数必须是查询结果集)
            screen_queryset = self.filter_queryset(queryset)
            # 判断所需数据类型
            if data_category == "all":
                # 子序列化器，用来对外键数据进行规范
                creator_serializer = my_serializer(WangtoUser, field=["nick_name"], is_child=True)
                # 分页后的查询结果集
                page = self.paginate_queryset(screen_queryset)
                # 设定序列化条件
                serializer = my_serializer(WangtoOperator, many=True,
                                           field=["id", "nick_name", "account", "register_time", "expire_time",
                                                  "state"],
                                           childs={"creator": (creator_serializer, False)})
                # 存在分页查询
                if page is not None:
                    serializer.instance = page
                    return self.get_paginated_response(serializer)
                return Response({
                    "code": 403,
                    "data": "必须携带分页数量参数"
                })
            elif data_category == "drop":
                serializer = my_serializer(WangtoOperator, screen_queryset, many=True, excludes=("id", "state"))
                return Response({
                    "code": 200,
                    "data": serializer.data
                })

    @check_bg_authorization_token
    def create(self, request, *args, **kwargs):
        # 权限
        identity = request.identity
        # 用户实例
        user_obj = request.user_obj

        if identity == "admin":
            leader_id = request.data.get("leader")
            leader_obj = user_obj.my_leader.get(id=leader_id)
            owner_obj = user_obj

        elif identity == "leader":
            leader_obj = user_obj
            owner_obj = user_obj.creator

        else:
            return Response({
                "code": 401
            })

        operator_obj = WangtoOperator()
        operator_obj.owner = owner_obj
        operator_obj.creator = leader_obj
        operator_obj.save()
        # print(operator_obj)
        serializer = my_serializer(WangtoOperator, operator_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # operator_obj.owner = owner_obj
        # operator_obj.creator = leader_obj
        # operator_obj.save()
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        # TODO
        for f in serializer.data:
            print(serializer.data)
            if "time" in f:
                utcTime = sb.datetime.strptime(serializer.data[f], UTC_FORMAT)
                localtime = utcTime + sb.timedelta(hours=8)
                serializer.data[f] = localtime

        return Response({
            "code": 200,
            "data": serializer.data
        })

        # serializer = my_serializer(WangtoOperator, data={"nick_name": "hahaha"})
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        # 请求数据类型
        data_category = request.data_category
        # 判断权限
        if identity == "admin":
            # 需要序列化的查询结果集
            queryset = user_obj.my_leader.all()
            # 筛选后的查询结果集_queryset参数必须是查询结果集)
            screen_queryset = self.filter_queryset(queryset)
            # 判断所需数据类型
            if data_category == "all":
                pass
                # # 子序列化器，用来对外键数据进行规范
                # creator_serializer = my_serializer(WangtoUser, field=("nick_name",), is_child=True)
                # # 分页后的查询结果集
                # page = self.paginate_queryset(screen_queryset)
                # # 设定序列化条件
                # serializer = my_serializer(WangtoOperator, many=True,
                #                            field=["id", "nick_name", "account", "register_time", "expire_time",
                #                                   "state"],
                #                            childs={"creator": (creator_serializer, False)})
                # # 存在分页查询
                # if page is not None:
                #     serializer.instance = page
                #     return self.get_paginated_response(serializer)
                # return Response({
                #     "code": 403,
                #     "data": "必须携带分页数量参数"
                # })
            elif data_category == "drop":
                serializer = my_serializer(WangtoUser, screen_queryset, many=True, field=["nick_name", "account", "id"])
                return Response({
                    "code": 200,
                    "data": serializer.data
                })
