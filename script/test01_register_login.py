import unittest
import requests
from api.api_register_login import ApiRegisterLogin
from parameterized import parameterized
from util import read_json, clear_data
from api import log
import time

class TestRegisterLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls)->None:
        # 清除测试数据
        clear_data()

    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        log.info("正在初始化session对象: {}".format(self.session))
        # 获取ApiRegisterLogin实例
        self.reg = ApiRegisterLogin(self.session)

    # 结束
    def tearDown(self) -> None:
        self.session.close()
        log.info("正在关闭session对象: {}".format(self.session))


    # 1、获取图片验证码接口 测试
    @parameterized.expand(read_json('register_login.json', "img_code"))
    def test01_img_code(self, random, expect_code):
        try:
            # 1、调用图片验证码接口
            r = self.reg.api_img_code(random)
            log.info("执行图片验证码响应状态码为: {}".format(r.status_code))
            # 2、查看响应状态码
            self.assertEqual(expect_code, r.status_code)
            log.info("执行图片验证码断言通过")
        except Exception as e:
            # 日志
            log.error("断言失败，原因: {}".format(e))
            # 抛异常
            raise

    # 2、获取短信验证码接口 测试
    @parameterized.expand(read_json('register_login.json', "phone_code"))
    def test02_phone_code(self, phone, imgVerifyCode, expect_text):
        try:
            # 1、调用获取图片验证码接口 --目的：让session对象记录cookie
            self.reg.api_img_code(123)
            # 2、调用短信验证码接口
            r = self.reg.api_phone_code(phone=phone, imgVerifyCode=imgVerifyCode)
            log.info("执行接口结果为: {}".format(r.text))
            # 3、查看响应结果
            self.assertIn(expect_text, r.text)
            log.info("执行断言通过！")
        except Exception as e:
            # 日志
            log.error("断言失败，原因: {}".format(e))
            # 抛异常
            raise

    # 3、注册接口 测试
    @parameterized.expand(read_json('register_login.json', "register"))
    def test03_register(self,phone, password, verifycode, phone_code, expect_text):
        try:
            # 1、图片验证码接口
            self.reg.api_img_code(123)
            # 2、短信验证码接口
            self.reg.api_phone_code(phone=phone, imgVerifyCode=verifycode)
            # 3、注册接口
            r = self.reg.api_register(phone=phone, password=password, verifycode=verifycode, phone_code=phone_code)
            log.info("执行接口结果为: {}".format(r.text))
            # 4、查看结果
            self.assertIn(expect_text, r.text)
            log.info("执行断言通过！")
        except Exception as e:
            # 日志
            log.error("断言失败，原因: {}".format(e))
            # 抛异常
            raise

    # 4、登录接口 测试
    @parameterized.expand(read_json('register_login.json', "login"))
    def test04_login(self, keywords, password, expect_text):
        try:
            i = 1
            r = None
            if "error" in password:
                while i <= 3:
                    r = self.reg.api_login(keywords=keywords, password=password)
                    i = i + 1
                # 断言锁定
                print("测试锁定: ", r.text)
                self.assertIn("锁定", r.text)
                # 暂停60秒
                time.sleep(60)
                # 测试登录成功
                r = self.reg.api_login(keywords=keywords, password="test123")
                log.info("执行接口结果为: {}".format(r.text))
                # 断言登录成功
                self.assertIn(expect_text, r.text)
                log.info("执行断言通过！")
            else:
                # 1、调用登录接口
                r = self.reg.api_login(keywords=keywords, password=password)
                log.info("执行接口结果为: {}".format(r.text))
                # 2、查看结果
                self.assertIn(expect_text, r.text)
                log.info("执行断言通过！")
        except Exception as e:
            # 日志
            log.error("断言失败，原因: {}".format(e))
            # 抛异常
            raise

    # 5、查询登录状态接口 测试
    @parameterized.expand(read_json('register_login.json', "login_status"))
    def test05_login_status(self,  status, expect_text):
        try:
            if status == "已登录":
                # 1、调用登录接口
                self.reg.api_login(keywords="15252292776", password="test123")
            # 2、调用查询登录状态接口
            r = self.reg.api_login_status()
            log.info("执行接口结果为: {}".format(r.text))
            # 3、查看结果
            self.assertIn(expect_text, r.text)
            log.info("执行断言通过！")
        except Exception as e:
            # 日志
            log.error("断言失败，原因: {}".format(e))
            # 抛异常
            raise