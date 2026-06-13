import unittest
import requests
from api.api_register_login import ApiRegisterLogin
from api.api_approve_trust import ApiApproveTrust
from api.api_tender import ApiTender
from parameterized import parameterized
from util import read_json,parser_html
from api import log

class TestTenderList(unittest.TestCase):
    def setUp(self):
        # 获取session对象
        self.session = requests.session()
        log.info("正在初始化session对象: {}".format(self.session))
        # 获取ApiRegisterLogin实例
        self.reg = ApiRegisterLogin(self.session)
        # 获取ApiApproveTrust对象
        self.approve = ApiApproveTrust(self.session)
        # 获取 ApiTender对象
        self.tender = ApiTender(self.session)

    def tearDown(self):
        self.session.close()
        log.info("正在关闭session对象: {}".format(self.session))

    def test01_tender_list(self):
        phone = "15252292778"
        password = "test123"
        card_id = "140404200507304957"
        # 1、获取图片验证码成功（随机小数）
        r = self.reg.api_img_code(0.123)
        # 2、获取短信验证码成功
        r = self.reg.api_phone_code(phone, 8888)
        # 3、注册成功（必填参数）
        r = self.reg.api_register(phone, password, 8888, 666666)
        # 4、登录成功
        r = self.reg.api_login(phone, password)
        # 5、认证成功
        r = self.approve.api_approve(card_id)
        # 6、请求后台开户
        r = self.approve.api_trust()
        # 7、三方开户
        result = parser_html(r)
        r = self.session.post(result[0], data=result[1])
        log.info("三方开户的结果为: {}".format(r.text))
        self.assertIn("OK", r.text)
        # 8、获取图片验证码成功（随机小数）
        r = self.approve.api_img_code(8888)
        # 9、后台充值响应成功
        r = self.approve.api_recharge(8888)
        # 10、三方充值
        result = parser_html(r)
        r = self.session.post(result[0], data=result[1])
        log.info("三方充值的结果为: {}".format(r.text))
        self.assertIn("OK", r.text)
        # 11、请求后台投资响应成功
        r = self.tender.api_tender(100)
        # 12、三方投资
        result = parser_html(r)
        r = self.session.post(result[0], data=result[1])
        log.info("三方投资的结果为: {}".format(r.text))
        self.assertIn("OK", r.text)
        log.info("断言通过！")