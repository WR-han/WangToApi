from rest_framework import serializers
from rest_framework import pagination
from rest_framework.response import Response


def my_serializer(_model=None, instance=None, many=False, data=None, field=None, _depth=None, allow=(), excludes=(),
                  childs=None, is_child=False, partial=False):
    """
    通用序列化器
    :param _model: 所需序列化的model对象
    :param instance: 查询结果集/查询结果对象 (实例)
    :param many: 序列化器many参数   =>(GET)
    :param data: 接收到的json   =>(PUT/POST)
    :param field: 需要查询的字段名范围 (可迭代对象)/如果需要加载子序列化器，此参数必须为列表    =>(GET)
    :param _depth: 外键层级   =>(GET)
    :param allow: 允许修改的字段   =>(PUT/POST)
    :param excludes: 排除字段   =>(GET)
    :param childs: 加载子序列化器   =>(GET)
        格式   =>(dict {"需要使用子序列化器的外键file_name":("自定义的子序列化器类","True/False 对应35行的many=")
    :param is_child: 是否为创建子序列化器
    :param partial: 是否允许部分字段更新   =>(POST/PUT)
    :return: 序列化器对象
    :return: 有is_child字段时 返回序列化器类
    """

    class GeneralSerializer(serializers.ModelSerializer):

        # 加载子序列化器
        if childs:
            for f in childs:
                # 如果有需要查询的字段名范围
                if field:
                    # 在查询的字段名范围中加入需要使用子序列化器的字段
                    field.append(f)
                locals()[f] = childs[f][0](many=childs[f][1])

        # 时间格式化
        if field:
            for f in field:
                if "time" in f:
                    locals()[f] = serializers.DateTimeField(format="%Y-%m-%d %X")

        class Meta:
            """
            model: 数据库绑定
            fields: 查询字段选择
            exclude: 查询字段筛选
            """
            model = _model

            # 有指定的查询字段
            if field:
                fields = field

            # 无指定的查询字段
            else:
                # 有data参数(POST/PUT) 允许所有字段
                if data:
                    fields = "__all__"

                # 无data参数(GET) 设置排除字段
                else:
                    if excludes:
                        exclude = excludes
                    else:
                        fields = "__all__"

            if _depth:
                depth = _depth

    # 作为子序列化器
    if is_child:
        return GeneralSerializer

    # POST / PUT
    if data:
        allow = set(allow)
        _data = {}

        # allow存在 且 json键超出allow范围
        if allow and (not allow.issuperset(set(data.keys()))):
            for key in allow:
                # 取出data中键名与allow对应的数据
                if key in data.keys():
                    _data[key] = data[key]
            return GeneralSerializer(data=_data, instance=instance, partial=partial)

        else:
            return GeneralSerializer(data=data, instance=instance, partial=partial)

    # GET
    else:
        ser = GeneralSerializer(instance=instance, many=many)
        # 加入表头字段供前端使用
        field_header = []
        for f in field:
            # id不进行展示 外键字段需前端按需展示
            if f != "id" and f not in childs.keys():
                field_header.append((f, getattr(_model, f).field.verbose_name))
        setattr(ser, "field_header", field_header)
        return ser


class MyPagination(pagination.LimitOffsetPagination):
    """
    自定义分页结果格式
    """

    # 重写分页后的返回数据json样式
    def get_paginated_response(self, serializer):
        try:
            field_header = serializer.field_header
        except Exception as e:
            field_header = [f"{e}"]
        return Response({
            "code": 200,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.count,
            "data": serializer.data,
            "field_header": field_header
        })
