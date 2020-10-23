from you_get.extractors import bilibili
import requests
import re


class Bilibili(object):

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        }
        self.download_header = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://www.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            # 'Referer': f'{self.url}',  # 视频地址
            'Accept-Encoding': 'identity',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Range': f'bytes=0-{self.size}',  # 视频长度
        }

    def get_video(self, video_url, download_url, req_range):
        temp = {'Referer': f'{video_url}', 'Range': f'bytes=0-{req_range}'}
        self.download_header.update(temp)
        res = requests.get(url=download_url, headers=self.download_header, stream=True).content
        return res

    def get_info(self, url):
        video_urls = []

        # 获取缩略图
        response = requests.get(url=url, headers=self.header).text  # 类型为str
        duration = int(re.search(r'(?<="timelength":).*?(?=,)', response).group())  # 获取时长
        pic_url = re.search(r'(?<=itemprop="image" content=").*?(?=">)', response).group(0)
        pic = requests.get(url=pic_url, headers=self.header).content  # 获取封面图
        with open('./temp/pic.jpg', 'wb') as f:
            f.write(pic)

        info = eval(bilibili.download(url, json_output=True))
        name = info['title']
        for i in info['streams'].values():
            q = i['quality'][3:] + ' ' + i['container']
            temp = [url, q, i['size'], i['src'][0]]  # 分别为视频原地址，视频质量，大小，下载地址
            video_urls.append(temp)
        return name, duration, video_urls

if __name__ == '__main__':
    app = Bilibili()
    app.get_info("https://www.bilibili.com/video/BV1zV411k7pr")
