from api import log
from config import HOST

class ApiRegisterLogin(object):
    # 初始化
    def __init__(self, session):
        # 获取Session对象
        self.session = session
        # 图片验证码url
        self.__url_img_code = HOST + "/common/public/verifycode1/{}"
        # 短信验证码url
        self.__url_phone_code = HOST + "/member/public/sendSms"
        # 注册url
        self.__url_register = HOST + "/member/public/reg"
        # 登录url
        self.__url_login = HOST + "/member/public/login"
        # 登录状态url
        self.__url_login_status = HOST + "/member/public/islogin"

    # 1、获取图片验证码接口 封装
    def api_img_code(self, random):
        log.info("正在调用获取图片验证码接口，请求方法: {} 请求url: {}".format("get", self.__url_img_code.format(random)))
        # 调用get方法
        return self.session.get(url = self.__url_img_code.format(random))

    # 2、获取短信验证码接口 封装
    def api_phone_code(self, phone, imgVerifyCode):
        # 1、定义请求参数
        data = {
            "phone": phone,
            "imgVerifyCode": imgVerifyCode,
            "type": "reg"
        }
        log.info("正在调用获取短信验证码接口，请求方法: {} 请求url: {} 请求参数: {}".format("post", self.__url_phone_code, data))
        # 2、调用请求方法
        return self.session.post(url = self.__url_phone_code, data = data)

    # 3、注册接口 封装
    def api_register(self, phone, password, verifycode,phone_code):
        # 1、定义请求参数
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code":phone_code,
            "dy_server": "on",
            "invite_phone": "",
        }
        log.info("正在调用注册接口，请求方法: {} 请求url: {} 请求参数: {}".format("post", self.__url_register, data))
        # 2、调用请求方法
        return self.session.post(url = self.__url_register, data = data)

    # 4、登录接口 封装
    def api_login(self, keywords="15252292771", password="test123"):
        # 1、定义请求参数
        data = {
            "keywords": keywords,
            "password": password,
        }
        log.info("正在调用登录接口，请求方法: {} 请求url: {} 请求参数: {}".format("post", self.__url_login, data))
        # 2、调用请求方法
        return self.session.post(url=self.__url_login, data=data)

    # 5、查询登录状态接口 封装
    def api_login_status(self):
        log.info("正在调用查询登录状态接口，请求方法: {} 请求url: {}".format("post", self.__url_login_status))
        return self.session.post(url=self.__url_login_status)