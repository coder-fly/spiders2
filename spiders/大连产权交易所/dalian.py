"""
@desc:https://www.daee.cn/article/xmdt/zczr/?sysEname=UTRL&pageSize=16&proType=&TypeGz=&template=&pageIndex=4
"""
import re
import base64

import requests
import execjs
from Crypto.Cipher import AES


class DaLianChanQuanSpider:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "https://www.daee.cn/article/xmdt/zczr/?sysEname=UTRL&pageSize=16&proType=&TypeGz=&template=&pageIndex=4"
    }
    base_url = "https://www.daee.cn/article/xmdt/zczr/?sysEname=UTRL&pageSize=16&proType=&TypeGz=&template=&pageIndex=4"
    session = requests.session()
    session.headers = headers
    session.verify = False

    def start(self):
        response = self.session.get(self.base_url)
        get_key = re.search(r'function get_key([\s\S]*?)return', response.text).group(1)
        get_key, param_key = get_key.split(" = CryptoJS.enc.Utf8.parse(")[0], \
                             get_key.split(" = CryptoJS.enc.Utf8.parse(")[1]
        param_key = param_key.split(")")[0]
        if "encrypt_key" in get_key:
            get_key = get_key.strip("encrypt_key") + "return " + param_key + "}"
        else:
            get_key = get_key.strip("var fksy") + "return " + param_key + "}"

        get_key = "function get_key" + get_key
        auth_url = re.search(r'auth_url = "/([\s\S]*?)"', response.text).group(1)
        ctx = execjs.compile(get_key)
        key = ctx.call("get_key")
        text = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82_*_zh-CN_*_24_*_8_*_1_*_12_*_1920,1080_*_1920,1040_*_-480_*_Win32_*_Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf,Chrome PDF Viewer::_*_8ef177d84bfc2d08f9a348a3f6ecacad_*_048c5b77f33a2db9a2df8e2d46596518_*_Google Inc.~ANGLE (NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0)_*_false_*_false_*_false_*_false_*_false_*_0,false,false_*_Arial,Arial Black,Arial Narrow,Calibri,Cambria,Cambria Math,Comic Sans MS,Consolas,Courier,Courier N"
        iv = "6532897456985214"
        wafatclconfirm = self.encrypt(key, iv, text)
        self.session.cookies.update({
            "wafatclconfirm": wafatclconfirm
        })
        self.session.get("https://www.daee.cn/{}".format(auth_url))

        print(self.session.cookies.get_dict())
        print(self.session.get(self.base_url).text)

    def encrypt(self, key, iv, text):
        text = self.pkcs7_padding(text.encode('utf-8'))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        return base64.b64encode(cipher.encrypt(text)).decode()

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len] * pad_len)
        return data

if __name__ == '__main__':
    spider = DaLianChanQuanSpider()
    spider.start()