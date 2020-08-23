import requests
import re
import os


class bilibiliVideo(object):

    def __init__(self):
        self.header1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        }
        self.header2 = {
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
        self.url = None
        # self.video_url = []  # 112:1080p+ 80:1080p 64:720p 32:480p 16:360p
        # self.audio_url = []  # 30280: 160kbps 30216: 80kbps
        self.filename = None
        # self.size = None
        # self.vq = 0  # 视频质量: 0:最高画质优先 1:1080p+ 2:1080p 3:720p 4:480p 5:360p
        # self.aq = 0  # 音频质量: 0:最高音质优先 1:160kbps 2:80kbps
        self.duration = None

    def get_video(self, url, size):
        self.header2.update({'Range': f'bytes=0-{size}'})
        res = requests.get(url=url, headers=self.header2, stream=True)
        return res
        # print(res.headers)
        # with open('./temp/video.flv', 'wb') as f:
        #     for data in res.iter_content(1024):
        #         f.write(data)

    def get_audio(self, url, size):
        self.header2.update({'Range': f'bytes=0-{size}'})
        res = requests.get(url=url, headers=self.header2)
        return res
        # with open('./temp/audio.mp3', 'wb') as f:
        #     for data in res.iter_content(1024):
        #         f.write(data)

    def get_info(self, url):
        video_url = []
        audio_url = []
        self.url = url  # 视频地址
        self.header2.update({'Referer': f'{self.url}'})  # 插入Referer
        response = requests.get(url=self.url, headers=self.header1).text  # 类型为str
        # print(response)
        res = eval(re.search(r'(?<=window.__playinfo__=).*?(?=</script><script>)', response).group())["data"]["dash"]  # 类型为dict
        # print(res)
        pre_id = 0
        now_id = 0
        for i in res["video"]:
            temp = [i["id"], i["baseUrl"], i["bandwidth"]]
            now_id = i["id"]
            if now_id != pre_id:
                video_url.append(temp)
                pre_id = now_id
            else:
                continue
        # print(self.video_url)
        pre_id = 0
        now_id = 0
        for i in res["audio"]:
            temp = [i["id"], i["baseUrl"], i["bandwidth"]]
            now_id = i["id"]
            if now_id != pre_id:
                audio_url.append(temp)
                pre_id = now_id
            else:
                continue
        # print(self.audio_url)
        self.filename = re.search(r'(?<="title":").*?(?=",)', response).group(0)  # 获取名字
        # print(self.filename)
        self.duration = int(re.search(r'(?<="timelength":).*?(?=,)', response).group())  # 获取时长
        pic_url = re.search(r'(?<=itemprop="image" content=").*?(?=">)', response).group(0)
        pic = requests.get(url=pic_url, headers=self.header1).content  # 获取封面图
        with open('./temp/pic.jpg', 'wb') as f:
            f.write(pic)
        return self.filename, self.duration, video_url, audio_url


if __name__ == '__main__':
    app = bilibiliVideo()
    name, duration, video_url, audio_url = app.get_info("https://www.bilibili.com/video/BV1fZ4y1u7nc")
    video_size = int((duration / 1000) * video_url[0][2] / 8)
    app.get_video(video_url[0][1], video_size)
