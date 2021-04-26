#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: selenium_test
@time: 2021/3/16
@email: coderflying@163.com
@desc: 
"""
import time

from selenium.webdriver import Chrome, ChromeOptions

from spiders.猿人学 import get_session

options = ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches",['enable-automation'])
options.add_argument("--headless")  # 无界面
driver = Chrome(chrome_options=options)

session = get_session()
result = 0
driver.get('http://59.110.158.68/')

with open("selenium_exec.js", "r", encoding="utf-8") as f:
    js = f.read()
driver.execute_script(js)
session.cookies.update({
    "sessionid":"zyamha3gpgomj21sxy60tooiyykq318t"
})
for i in range(1, 6):

    response = session.get('http://match.yuanrenxue.com/api/match/14/m')


    eval_m =  "window.eval_m=function(){" + response.text + "}"
    driver.execute_script(eval_m)
    m_str = driver.execute_script("return window.sp()")
    print(m_str)

    session.cookies.update({
        "m":m_str,
        "mz":"TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg4LjAuNDMyNC4xOTAgU2FmYXJpLzUzNy4zNixbb2JqZWN0IE5ldHdvcmtJbmZvcm1hdGlvbl0sdHJ1ZSwsW29iamVjdCBHZW9sb2NhdGlvbl0sMTYsemgtQ04semgtQ04semgsMCxbb2JqZWN0IE1lZGlhQ2FwYWJpbGl0aWVzXSxbb2JqZWN0IE1lZGlhU2Vzc2lvbl0sW29iamVjdCBNaW1lVHlwZUFycmF5XSx0cnVlLFtvYmplY3QgUGVybWlzc2lvbnNdLFdpbjMyLFtvYmplY3QgUGx1Z2luQXJyYXldLEdlY2tvLDIwMDMwMTA3LFtvYmplY3QgVXNlckFjdGl2YXRpb25dLE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84OC4wLjQzMjQuMTkwIFNhZmFyaS81MzcuMzYsR29vZ2xlIEluYy4sLFtvYmplY3QgRGVwcmVjYXRlZFN0b3JhZ2VRdW90YV0sW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSw4MjUsLTE1MzYsNSwxNTM2LDI0LDg2NSxbb2JqZWN0IFNjcmVlbk9yaWVudGF0aW9uXSwyNCwxNTM2LFtvYmplY3QgRE9NU3RyaW5nTGlzdF0sZnVuY3Rpb24gYXNzaWduKCkgeyBbbmF0aXZlIGNvZGVdIH0sLG1hdGNoLnl1YW5yZW54dWUuY29tLG1hdGNoLnl1YW5yZW54dWUuY29tLGh0dHA6Ly9tYXRjaC55dWFucmVueHVlLmNvbS9tYXRjaC8xNCxodHRwOi8vbWF0Y2gueXVhbnJlbnh1ZS5jb20sL21hdGNoLzE0LCxodHRwOixmdW5jdGlvbiByZWxvYWQoKSB7IFtuYXRpdmUgY29kZV0gfSxmdW5jdGlvbiByZXBsYWNlKCkgeyBbbmF0aXZlIGNvZGVdIH0sLGZ1bmN0aW9uIHRvU3RyaW5nKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gdmFsdWVPZigpIHsgW25hdGl2ZSBjb2RlXSB9"


    })

    params = {
        "page":i
    }

    response = session.get('http://match.yuanrenxue.com/api/match/14', params=params).json()
    print(response)
    result += sum([item['value'] for item in response['data']])
    time.sleep(1)
print(result)



driver.quit()
# 247986