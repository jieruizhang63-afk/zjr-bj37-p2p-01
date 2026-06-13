import unittest
import requests

from api import log
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util import parser_html,read_json
from parameterized import parameterized


class TestTender(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.Session()
        log.info("正在初始化session对象: {}".format(self.session))
        # 获取 ApiTender对象
        self.tender = ApiTender(self.session)
        # 调用登录
        ApiRegisterLogin(self.session).api_login()

    # 结束
    def tearDown(self) -> None:
        self.session.close()
        log.info("正在关闭session对象: {}".format(self.session))

    # 测试方法
    @parameterized.expand(read_json("tender.json", "tender"))
    def test01_tender(self, amount, expect_text):
        try:
            # 调用投资方法
            r = self.tender.api_tender(amount=amount)
            log.info("接口执行结果为: {}".format(r.json()))
            if amount == 100:
                # 断言
                self.assertIn("form", r.text)
                log.info("断言通过！")
                # 调用三方投资
                result = parser_html(r)
                # 期望 (http://xxxxxx,{"Version":10,})
                r = self.session.post(result[0], data=result[1])
                log.info("三方投资的结果为: {}".format(r.text))
                self.assertIn(expect_text, r.text)
                log.info("断言通过！")
            else:
                self.assertIn(expect_text, r.text)
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise