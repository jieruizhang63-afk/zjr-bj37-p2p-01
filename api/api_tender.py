from config import HOST

class ApiTender:
    # 初始化
    def __init__(self, session):
        # session
        self.session = session
        # url
        self.__url_tender = HOST + "/trust/trust/tender"

    # 1、投资方法
    def api_tender(self, amount):
        # 1、参数
        data = {
            "id":642,
            "depositCertificate":-1,
            "amount":amount,
        }
        # 2、调用请求方法
        return self.session.post(url=self.__url_tender, data=data)