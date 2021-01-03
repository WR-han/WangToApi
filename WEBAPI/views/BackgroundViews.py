import hmac

from tool.authorization_token import *
from rest_framework import response
from rest_framework.views import APIView


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
            print(account, password)
            account_obj = WangtoUser.objects.get(account=account)
            if password == account:
                print(1)
                password_h = password
            else:
                print(2)
                h = hmac.new(salt, password.encode(), digestmod="sha256")
                password_h = h.hexdigest()

            # 密码比对
            if account_obj.passworld == password_h:
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
