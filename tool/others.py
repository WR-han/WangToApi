import hmac
from key.key import salt
from rest_framework import pagination
from rest_framework.response import Response


def get_model_field(model_obj, need_field, exclude_filed):
    """
    获取model的verbose_name和name的字段
    """
    filed = model_obj._meta.fields
    if filed:
        field_dic = []
        exclude = list(exclude_filed)
        params = [f for f in filed if ((f.name in need_field) and (f.name not in exclude))]

        for i in params:
            field_dic.append((i.name, i.verbose_name))
        return field_dic
    else:
        return None


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


def create_password(password):
    h = hmac.new(salt, password.encode(), digestmod='sha256')
    m_ps_h = h.hexdigest()
    return m_ps_h
