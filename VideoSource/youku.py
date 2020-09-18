import requests
import os
import time
import random
import re
from Crypto import Cipher
from urllib import request
from hashlib import md5

class Youku(object):

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Referer': 'https://v.youku.com/v_show/id_XMzEyMzk5Mjg0NA==.html',
            'Host': 'acs.youku.com',
            'Cookie': '_m_h5_tk=6fc37ffda368c28fc9f52baf5d79ddfc_1600153583047; _m_h5_tk_enc=60c804ecc9645f96ca0778b1eb7bea54; Domain=youku.com;'
        }
        # self.url = 'https://v.youku.com/v_show/id_XMzEyMzk5Mjg0NA==.html'
        self.time = int(time.time())
        # self.ckey = "7B19C0AB12633B22E7FE81271162026020570708D6CC189E4924503C49D243A0DE6CD84A766832C2C99898FC5ED31F3709BB3CDD82C96492E721BDD381735026"
        self.vid = "XMzEyMzk5Mjg0NA=="
        self.token = "6fc37ffda368c28fc9f52baf5d79ddfc"
        self.data = {
	"steal_params": "{\"ccode\":\"0502\",\"client_ip\":\"192.168.1.1\",\"utid\":\"NBevFStAZEQCAW40jnu9IcNS\",\"client_ts\":1566290208,\"version\":\"1.8.1\",\"ckey\":\"119#MlKT3NBFM8PGzMMzlyfMRuVLT7EBEbACc6MtYBAsqUnTFatOwvVDvYyAjcplNL8GLeASRBsU3AALuwHNk9SKOrA8RJBONt8L9ei25SSUdGIy/Upp4SMn6rA2RW1zNNFGfeAzR/QYdUeIx4LL7G12qCnxSCqOfoDjsvmw6EOMAOl7Y/h6SYVHIxImmtyIKrTJDojBBgjZTamxD7tViyQxxP+C3W/fByo7iM3PGDP3dzMNrb0Y96bE7k8oJV6e6IaFwcLCuRUspdmc4zcGhpzU4m/8TqqD0cuYnEwbg+pQHpkBd9ALU3j6uFCi9h6jIaRrpTSV7kwAur6WcTODqT1B4d6/MJ9eFwkMZrVn5MabjVXDbKcnmaGmL9aj/4k1yfWkCY0YNhREFvU7N/slngR/mgjDBGPBvvm5CR4PHRrTE4c7DCfnW/xEW31J19xRLyc2P48mIQM2LQxfw2cBJhCDrxZXJBEWyA3XplF7/8a9D5z0BU0THL6GE4ec/ru6n9yNWaSMq5mY/uJNNf9wh3GymAu4hJTGV35dOFSIhSrYsMa3r/Icy4BmbcxCzxIw9f4xqeQxFBo8d8501Zl2vKkrOO2WMrom3RkH1OBfOLUwjPSJqOZ1Y7HFSE0RkD+FHtNhZdE1bTjG3FW56JBXao90g1tWjedX+Q14g9QTbhVSrzkXBbMUIC==\"}",
	"biz_params": "{\"vid\":\"XMzEyMzk5Mjg0NA==\",\"play_ability\":5376,\"master_m3u8\":1,\"media_type\":\"standard,subtitle\",\"app_ver\":\"1.8.1\"}",
	"ad_params": "{\"vs\":\"1.0\",\"pver\":\"1.8.1\",\"sver\":\"2.0\",\"site\":1,\"aw\":\"w\",\"fu\":0,\"d\":\"0\",\"bt\":\"pc\",\"os\":\"win\",\"osv\":\"7\",\"dq\":\"auto\",\"atm\":\"\",\"partnerid\":\"null\",\"wintype\":\"interior\",\"isvert\":0,\"vip\":0,\"emb\":\"AjEwNzk3MDM3NzMCdi55b3VrdS5jb20CL3Zfc2hvdy9pZF9YTkRNeE9EZ3hOVEE1TWc9PS5odG1s\",\"p\":1,\"rst\":\"mp4\",\"needbf\":2}"
}
        pre = f"{self.token}&{self.time}&24679788&{self.data}"
        print(pre)
        self.sign = md5().hexdigest()
        print(self.sign)
        # self.url = f'https://ups.youku.com/ups/get.json?vid={self.vid}&ccode=0501&client_ip=192.168.1.1&client_ts={self.time}&utid={self.utid}&ckey={self.ckey}'
        self.url = f'http://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?&appKey=24679788&t={self.time}&sign={self.sign}&api=mtop.youku.play.ups.appinfo.get&data={self.data}'

    def get_info(self):
        res = requests.get(url=self.url, headers=self.header).text
        print(res)

    def get_video(self):
        pass

    def get_audio(self):
        pass


if __name__ == "__main__":
    run = Youku()
    # run.get_info()
