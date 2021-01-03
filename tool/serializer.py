from rest_framework import serializers


def my_serializer(_model, instance=None, many=False, data=None, field=None, _depth=None, allow=(), excludes=()):
    """
    通用序列化器
    :param _model: 所需序列化的model对象
    :param instance: 查询结果集/查询结果对象 (实例)
    :param many: 序列化器many参数 (GET)
    :param field: 需要查询的字段名 (GET)
    :param excludes: 排除字段 (GET)
    :param _depth: 外键层级 (GET)
    :param data: 接收到的json (PUT/POST)
    :param allow: 允许修改的字段 (PUT/POST)
    :return: 序列化器对象
    """

    class Serializer(serializers.ModelSerializer):

        # # 数据编辑
        # # name --> 返回json键名
        # # source --> 所绑定数据库字段名
        # # error_messages --> 自定义错误信息(字典)
        # m_ac= serializers.EmailField(max_length=50,error_messages={
        #     'max_length':'字段超长'
        # })

        # # 数据新增
        # # id_10 --> 新增json键名
        # # get_id_10 --> 数据编辑方法
        # id_10 = serializers.SerializerMethodField()
        # def get_id_10(self,instance):
        #     return instance.id * 10
        #
        # # 时间格式化
        # date = serializers.DateTimeField(format='%Y-%m-%d %X')

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
                    fields = '__all__'

                # 无data参数(GET) 设置排除字段
                else:
                    if excludes:
                        exclude = excludes
                    else:
                        fields = '__all__'

            if _depth:
                depth = _depth

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

            return Serializer(data=_data, instance=instance)

        else:
            return Serializer(data=data, instance=instance)

    # GET
    else:
        return Serializer(instance=instance, many=many)
