#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: baiduzhishu
@time: 2021/3/12
@email: coderflying@163.com
@desc:
"""
import requests


js = '''function decrypt(t, e) {
            for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++) a[n[o]] = n[n.length / 2 + o];
            for (var s = 0; s < e.length; s++) r.push(a[i[s]]);
            return r.join("")
        }'''

headers = {
    "Cookie": """PSTM=1609917594; BAIDUID=243F48DF2F4B734706E1DAF6823356D6:FG=1; BIDUPSID=EC2490949F76E5FAF76897136C7E23DE; BDUSS=lY4aG9oTGtFMjFYNlBjOHp5R1lPbFo1VDNRcUVjanVuR0Y0Q283Z2c5TVppa1ZnRUFBQUFBJCQAAAAAAAAAAAEAAAADdJ8hNzg1OTk0NTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABn9HWAZ~R1gU; MCITY=-131%3A; H_WISE_SIDS=110085_114550_127969_131423_144966_154213_156286_156927_160879_162898_163305_163569_164325_164955_165136_165328_166148_166155_166184_167069_167086_167112_167301_168034_168205_168542_168576_168626_168747_168762_169308_169612_169670_169788_170012_170155_170241_170243_170286_170292_170415_170476_170547_170578_170581_170582_170589_170606_170707_170917_170958; ZD_ENTRY=baidu; delPer=0; PSINO=2; BDRCVFR[r3VqGGrxDQ3]=mk3SLVN4HKm; BDRCVFR[S4-dAuiWMmn]=xEs-eb58IM0fjmYnjTdnH0Lg17xuAT; H_PS_PSSID=33636_33344_31253_33692_33595_33570_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=a02laha525042k2lr41g4m3mu0q; BCLID=8002461440669789525; BDSFRCVID=3fPOJeCwM9rn4mJesIqstKoWoKzsSDOTH6aoemgQNU-YDK-ucAtdEG0PVU8g0K4-S2-LogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tJ-J_IPKJD-3jRjd5bO2qRIJMfcKbJQKaDQ03Ru8Kb7VbpI6jMnkbfJBDGO8aPvnQIT9L-JvJxJJMRRN5UrRbjK7yajK2-cqaDoxLKIM2UJMStnOW-RpQT8r0pAOK5OibCrj0M3sab3vOIJzXpO156kzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqjFetb4HoCv5b-0_HJT4-P7Eh4oH-UnLetJXf5Risl7F5l8-hCQvbqrW-4Lg5gcZtlOMJDJ-2CTn-K3xOKQphpoz2bIXjRoN2lbTfmQQ2b6N3KJmb-P9bT3v5Drbyq7L2-biWbRL2MbdbDnP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhbLGe6L5e5o3DGtsKC6aKC5bL6rJabC3hnQMXU6qLn-Ieq5XtPrZ567AQ4O2Wb7RDpvuKpbUXp0njxQyK4rMLmoPsxTgW56hHpjmbMonDh8Z3H7MJUPJHGAHslRO5hvvhb6O3M7-qfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_E5bj2qRAfVIty3H; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1615531754; bdindexid=5v284tgcjcvbuviit1idju5cd3; RT="z=1&dm=baidu.com&si=co6nv5ygbaw&ss=km5xw5ju&sl=4&tt=4ee&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1615531767; __yjsv5_shitong=1.0_7_b4113dcd7b894efe3eb8d0d255c780abb1e1_300_1615531766771_61.50.117.3_bde44260""",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
data_url = 'https://index.baidu.com/api/SearchApi/index?word={}&area=0&days=30'
uniqid_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'


keys = ["all","pc","wise"]

class BaiDuIndex(object):

    def __init__(self):
        self.session = self.get_session()

    def decrypt(self, t: str, e: str) -> str:
        n, i = t, e
        a = {}
        o = 0
        r = []
        while o < len(n) / 2:
            a[n[o]] = n[len(n) // 2 + o]
            o += 1
        for s in range(len(e)):
            r.append(a[i[s]])
        return "".join(r)

    def do_request(self,url):
        return self.session.get(url)

    def parse(self,response,uniqid):
        result = []
        data_dict = response.get("data").get("userIndexes")[0]
        for key in keys:
            result.append({key:self.decrypt(uniqid,data_dict.get(key).get("data"))})
        return result

    def get_baidu_index(self,keyword):
        response = self.do_request(data_url.format(keyword)).json()
        uniqid = self.do_request(uniqid_url.format(response.get("data").get("uniqid"))).json().get("data")
        return self.parse(response,uniqid)


    @staticmethod
    def get_session():
        session = requests.session()
        session.headers =headers
        session.verify = False
        return session

if __name__ == '__main__':
    baidu = BaiDuIndex()
    print(baidu.get_baidu_index('[[{"name":"大众","wordType":1}]]'))
