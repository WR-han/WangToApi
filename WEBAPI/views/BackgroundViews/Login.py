from rest_framework.response import Response
from rest_framework.views import APIView
from WEBAPI.models import WangtoUser
from tool.authorization_token import make_bg_authorization_token
from tool.others import create_password


class Login(APIView):
    """
    用户登录
    """

    def post(self, request):
        """
        账号登陆
        """
        # json格式检查
        try:
            password = request.data["password"]
            account = request.data["account"]
        except Exception as e:
            return Response({
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
                password_h = create_password(password)

            # 密码比对
            if account_obj.password == password_h:
                # 生成token
                token = make_bg_authorization_token(wangto_user_id=account_obj.pk)
                return Response({
                    "code": 200,
                    "token": token,
                    "identity": account_obj.identity
                })

            else:
                return Response({
                    "code": 401,
                    "data": "密码错误"
                })

        except Exception as e:
            return Response({
                "code": 401,
                "data": "用户不存在",
                "msg": f"{e}"
            })
