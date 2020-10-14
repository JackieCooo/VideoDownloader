import requests
import re
import os
from hashlib import md5


class Iqiyi(object):

    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    def get_info(self, url):
        pass

    def get_video(self):
        pass

    def get_audio(self):
        pass


if __name__ == "__main__":
    run = Iqiyi()
    run.get_info('https://www.iqiyi.com/v_1325ib07fxk.html')