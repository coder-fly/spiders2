#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: multi
@time: 2021/1/11
@email: coderflying@163.com
@desc: 
"""
#!usr/bin/env python
# -*- coding:utf-8 -*-
from urllib.parse import quote

"""
@author: coderfly
@file: multi
@time: 2021/1/9
@email: coderflying@163.com
@desc: 
"""
#!usr/bin/env python
# -*- coding:utf-8 -*-
from copy import deepcopy

"""
@author: coderfly
@file: multi
@time: 2020/12/18
@email: coderflying@163.com
@desc: 
"""
# encoding=utf-8
import json
import sys
import os
import subprocess
import time
import datetime
import pandas as pd
import logging
import logging.handlers
import requests
import traceback
from threading import Thread
from queue import Queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Content-Type': 'application/json',
}
url_queue = Queue()

def on_message(message, data):
    payload = message['payload']
    id, sign = payload.split(":")[0], quote(payload.split(":")[1])
    url_queue.put(url)




class Spider:
    url = 'https://sekiro.virjar.com/yuanrenxue/query?id={}&sign={}'

    def __init__(self):
        self.response_queue = Queue()  # 响应队列
        self.item_queue = Queue()  # item结果队列
        self.result = 0
        self.init_queue()

    def init_queue(self):
        for i in range(10000):
            sign = subprocess.getoutput('java -jar unidbg-android.jar {}'.format(i))
            url = self.url.format(i, sign)
            print(url)
            url_queue.put(url)


    def parse_url(self):
        """从url队列中取出待采集url，发送请求 存入response队列"""
        while True:
            try:
                url = url_queue.get()
                response = requests.get(url, headers=headers).json()
                self.response_queue.put(response)
            except Exception as e:
                print(e)
            finally:
                url_queue.task_done()

    def parse_response(self):
        """解析response为item线程"""
        while True:
            try:
                response = self.response_queue.get()
                item = int(response['data'])
                print(item)
                self.item_queue.put(item)
            except Exception as e:
                print(e)
            finally:
                self.response_queue.task_done()

    def save_data(self):
        """数据持久化线程"""
        while True:
            try:
                item = self.item_queue.get()
                self.result += item
            except Exception as e:
                print(e)
            finally:
                self.item_queue.task_done()

    def start_spider(self):
        """程序入口"""

        threads = []
        [threads.append(Thread(target=self.parse_url)) for _ in range(10)]  # 五个线程进行网络请求
        [threads.append(Thread(target=self.parse_response)) for _ in range(1)]  # 两个线程进行响应解析
        [threads.append(Thread(target=self.save_data)) for _ in range(1)]  # 两个线程进行数据持久化

        for t in threads:
            t.setDaemon(True)
            t.start()

        for q in [url_queue, self.response_queue, self.item_queue]:
            # 当任意一个队列不为空是，阻塞主线程，等在子线程完成对所有队列的处理
            q.join()
        time.sleep(5)
        print(self.result) # 4925000


if __name__ == '__main__':
    spider = Spider()
    spider.start_spider()

