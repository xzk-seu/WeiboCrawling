"""extractor"""
import re

from bs4 import BeautifulSoup

import res.Ban
from util.MyTime import MyTime


class Extractor:
    def __init__(self, interval=3):
        # print("Class:Extractor")
        self.__posts = []
        self.__is_too_old = False
        self.__interval = interval

    @ staticmethod
    def transform_str_to_int(str_num):
        if str_num is '':
            return 0
        else:
            return int(str_num)

    def is_too_old(self):
        return self.__is_too_old

    # 返回元祖构成的列表，每个元祖为一条微博。
    # 加上时间控制。
    def extractor(self, html):
        # 过滤规则
        pattern_ban = re.compile(res.Ban.ban_dengfeng, re.VERBOSE | re.IGNORECASE | re.DOTALL)
        pattern_nochinese = re.compile("[^\u4e00-\u9fa5\u3002-\u300B\uFF08-\uFF1F\u2013-\u201D]+")

        soup = BeautifulSoup(html, "lxml")
        # 用户名
        tag_nick_name = soup.select('a[class="W_f14 W_fb S_txt1"]')
        # 博文内容
        tag_content = soup.select('div[node-type="feed_list_content"]')
        # 时间，格式化的time获取 : time.attrs["title"]
        tag_time = soup.select('a[node-type="feed_list_item_date"]')
        # 转发数
        tag_num_forward = soup.select('span[node-type="forward_btn_text"] span')
        # 评论数 （将评论两个字过滤）
        tag_num_comment = soup.select('span[node-type="comment_btn_text"] span')
        # 赞数
        tag_num_like = soup.select('span[node-type="like_status"]')

        # 里层循环，每一条微博。
        for j in range(len(tag_content)):
            webo_content = pattern_nochinese.sub('', tag_content[j].getText().strip())

            # 如果博文内容中出现屏蔽词
            if pattern_ban.search(webo_content) is not None:
                continue

            nick_name = tag_nick_name[j].getText().strip()
            webo_time = tag_time[j].attrs["title"]
            num_forward = self.transform_str_to_int(tag_num_forward[j].getText().
                                                    replace('\u8f6c\u53d1', '').replace('\ue607', ''))
            num_comment = self.transform_str_to_int((tag_num_comment[j].getText().replace('\u8bc4\u8bba', '').
                                                     replace('\ue608', '')))
            num_like = self.transform_str_to_int(tag_num_like[j].getText()[1:].replace('\u8d5e', ''))

            if MyTime.interval(weibo_time=webo_time) <= self.__interval:
                self.__posts.append((nick_name, webo_content, webo_time, num_forward, num_comment, num_like))
                # print(nick_name, webo_content)
            elif MyTime.interval(weibo_time=webo_time) > self.__interval + 1:
                self.__is_too_old = True
        return self.__posts
