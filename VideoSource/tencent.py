import requests
import json


class Tencent(object):

    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'cookie': '',  # 下载vip资源需输入
            # 'referer': 'https://v.qq.com/x/cover/g1gf358prepzhvb/r31479y0ncs.html'
        }

    def get_info(self, url):
        vid = url[:-5].rsplit('/', 1)[1]
        self.header.update({'referer': url})
        video_url = []
        audio_url = []
        for q in ('fhd', 'shd', 'hd', 'sd'):
            params = {
                'isHLS': False,
                'charge': 1,
                'vid': vid,
                'defn': q,
                'defnpayver': 1,
                'otype': 'json',
                'platform': 10201,
                'sdtfrom': 'v1010',
                'host': 'v.qq.com',
                'fhdswitch': 0,
                'show1080p': 1,
            }
            res = requests.get(url='http://h5vv.video.qq.com/getinfo', headers=self.header, params=params)
            res = json.loads(res.content[len('QZOutputJson='):-1])
            print(res)
            prefix = res['vl']['vi'][0]['ul']['ui'][0]['url']
            suffix = res['vl']['vi'][0]['fn']
            vkey = res['vl']['vi'][0]['fvkey']
            size = res['vl']['vi'][0]['ul']['ui'][0]['fs']
            base_url = prefix + suffix + '?vkey=' + vkey
            temp = [base_url, size]
            video_url.append(temp)
        filename = res['vl']['vi'][0]['ti']
        duration = res['vl']['vi'][0]['td']
        return filename, duration, video_url, audio_url

    def get_video(self, url, size):
        res = requests.get(url=url, headers=self.header)
        return res


if __name__ == "__main__":
    run = Tencent()
    run.get_info('https://v.qq.com/x/cover/g1gf358prepzhvb/r31479y0ncs.html')
