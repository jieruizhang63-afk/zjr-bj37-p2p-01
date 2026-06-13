import unittest
import requests

from api import log
from api.api_approve_trust import ApiApproveTrust
from api.api_register_login import ApiRegisterLogin
from util import parser_html, read_json
from parameterized import parameterized


class TestApproveTrust(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 1、获取session
        self.session = requests.session()
        log.info("正在初始化session对象: {}".format(self.session))
        # 2、获取ApiApproveTrust对象
        self.approve = ApiApproveTrust(self.session)
        # 3、调用登录成功
        ApiRegisterLogin(self.session).api_login()

    # 结束
    def tearDown(self) -> None:
        self.session.close()
        log.info("正在关闭session对象: {}".format(self.session))

    # 1、认证测试
    def test01_approve(self):
        try:
            # 调用接口
            r = self.approve.api_approve()
            log.info("接口执行结果为: {}".format(r.text))
            # 断言
            self.assertIn("提交成功", r.text)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 2、查询认证状态接口 测试
    def test02_approve_status(self):
        try:
            # 调用接口
            r = self.approve.api_approve_status()
            log.info("接口执行结果为: {}".format(r.text))
            # 断言
            self.assertEqual(404, r.status_code)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 3、开户接口 测试
    def test03_trust(self):
        try:
            # 调用接口
            r = self.approve.api_trust()
            log.info("接口执行结果为: {}".format(r.json()))
            # 断言
            self.assertIn("form", r.text)
            log.info("断言通过！")
            # 三方开户
            result = parser_html(r)
            # 期望 (http://xxxxxx,{"Version":10,})
            r = self.session.post(result[0], data=result[1])
            log.info("接口执行结果为: {}".format(r.text))
            self.assertIn("OK", r.text)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 4、获取图片验证码接口 测试
    @parameterized.expand(read_json("approve_trust.json","img_code"))
    def test04_img_code(self, random, expect_text):
        try:
            # 调用接口
            r = self.approve.api_img_code(random)
            log.info("接口执行结果为: {}".format(r.text))
            # 断言
            self.assertEqual(expect_text, r.status_code)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 5、充值接口 测试
    @parameterized.expand(read_json("approve_trust.json", "recharge"))
    def test05_recharge(self, valicode, expect_text):
        try:
            # 调用获取图片验证码接口
            self.approve.api_img_code(0.123)
            # 调用接口
            r = self.approve.api_recharge(valicode)
            log.info("接口执行结果为: {}".format(r.json()))
            if valicode == 8888:
                # 断言
                self.assertIn("form", r.text)
                log.info("断言通过！")
                # 三方充值
                result = parser_html(r)
                # 期望 (http://xxxxxx,{"Version":10,})
                r = self.session.post(result[0], data=result[1])
                log.info("接口执行结果为: {}".format(r.text))
                self.assertIn(expect_text, r.text)
                log.info("断言通过！")
            else:
                self.assertIn(expect_text, r.text)
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise