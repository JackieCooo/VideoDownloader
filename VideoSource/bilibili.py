import requests, re, subprocess, json


class Bilibili(object):

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        }

    def get_info(self, url):
        video_urls = []

        # 获取缩略图
        response = requests.get(url=url, headers=self.header).text  # 类型为str
        duration = int(re.search(r'(?<="timelength":).*?(?=,)', response).group())  # 获取时长
        pic_url = re.search(r'(?<=itemprop="image" content=").*?(?=">)', response).group(0)
        pic = requests.get(url=pic_url, headers=self.header).content  # 获取封面图
        # with open('./temp/pic.jpg', 'wb') as f:  # 包内测试时注释
        #     f.write(pic)

        arg = f"you-get --json {url}"

        p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        info = json.loads(stdout)
        # print(stdout)
        # print(stderr)
        # print(type(info))

        name = info['title']
        for i, j in info['streams'].items():
            q = j['quality'][3:] + ' ' + j['container']
            temp = [q, j['size'], j['src'][0], i]  # 分别为视频质量，大小，下载地址，stream_id
            video_urls.append(temp)
        # print(video_urls)
        return name, duration, video_urls

if __name__ == '__main__':
    app = Bilibili()
    app.get_info("https://www.bilibili.com/video/BV1zV411k7pr")
