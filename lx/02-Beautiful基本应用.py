# 1、导包
from bs4 import BeautifulSoup
html = """
    <html>
        <head>
            <title>黑马程序员</title>
        </head>
        <body>
            <p id="test01">软件测试</p>
            <p id="test02">2020年</p>
            <a href="/api.html">接口测试</a>
            <a href="/web.html">Web自动化测试</a>
            <a href="/app.html">APP自动化测试</a>
        </body>
    </html>
"""

# 2、获取bs对象 告诉BeautifulSoup类，你要解析的是html格式
bs = BeautifulSoup(html, "html.parser")

# 3、调用方法
"""
    重点:
        1、查找所有标签 bs.find_all("标签名") == 元素的集合["元素1",“元素2”]
        2、查找属性 元素.get("属性名")
"""
for a in bs.find_all("a"):
    print(a.get("href"))

# 4、扩展其他方法
# 获取单个元素 bs.标签名
print(bs.a)
# 获取文本
print(bs.a.string)
# 获取属性
print(bs.a.get("href"))
# 获取标签名
print(bs.a.name)