from config import HOST


class ApiApproveTrust:
    # 初始化
    def __init__(self, session):
        # 获取session对象
        self.session = session
        # 认证url
        self.__url_approve = HOST + "/member/realname/approverealname"
        # 查询认证状态
        self.__url_approve_status = HOST + "/member/realname/getapprove"
        # 开户url
        self.__url_trust = HOST + "/trust/trust/register"
        # 图片验证码url
        self.__url_img_code = HOST + "/common/public/verifycode/{}"
        # 充值url
        self.__url_recharge = HOST + "/trust/trust/recharge"

    # 1、认证接口 封装
    def api_approve(self, card_id="140404200507028648"):
        # 1、请求参数
        data = {
            "realname":"张三",
            "card_id":card_id
        }
        # 2、调用请求方法 难题：multipart/form-data使用data+files来实现多消息体类型
        return self.session.post(url=self.__url_approve, data=data, files={"x":"y"})

    # 2、查询认证状态接口 封装
    def api_approve_status(self):
        return self.session.post(url=self.__url_approve_status)

    # 3、开户接口 封装
    def api_trust(self):
        return self.session.post(url=self.__url_trust)

    # 4、获取图片验证码接口 封装
    def api_img_code(self, random):
        return self.session.get(url=self.__url_img_code.format(random))

    # 5、充值接口封装
    def api_recharge(self,valicode):
        data = {
            "paymentType":"chinapnrTrust",
            "amount":1000,
            "formStr":"reForm",
            "valicode":valicode
        }
        return self.session.post(url=self.__url_recharge, data=data)