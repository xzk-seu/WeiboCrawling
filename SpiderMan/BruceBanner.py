# 提取微博地理标签页面“探索此地”的所有内容

from Avenger import Avengers
import time
import logging
import re
import os
from bs4 import BeautifulSoup
import json

logging.basicConfig(level=logging.DEBUG, filename='./logs/BruceBanner.txt',
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program, BruceBanner.')


class BruceBanner(Avengers):
    def __init__(self):
        super(BruceBanner, self).__init__()
        self.__urls_nearby = []

        self.__path_nearby = r"./data/html_nearby"
        self.__pages_nearby = []

    def get_page_nearby(self):
        for i in range(1, 11):
            content = self.get_page(self.urls['dengfengNearby'].format(page=i))
            logging.debug('get_page_nearby(): The len of content is ' + str(len(content)))
            tag = 0
            if tag < 5 and len(content) < 58000:
                content = self.get_page(self.urls['dengfengNearby'].format(page=i))
                tag += 1
            if len(content) > 58000:
                with open(self.__path_nearby + '/nearby_' + str(i) + '.txt', 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                logging.debug('get_page_nearby():第个文件' + str(i) + '写入失败。')
            time.sleep(10)
        print('get_page_nearby():________Done!________')

    def __load_page_nearby(self):
        list_page = os.listdir(self.__path_nearby)
        for page_name in list_page:
            with open(self.__path_nearby + '/' + page_name, 'r', encoding='utf-8') as f:
                self.__pages_nearby.append(f.read())
        print('__load_page_nearby():________页面已全部载入列表中！________')

    def get_urls_from_page_nearby(self):
        if len(self.__pages_nearby) is 0:
            self.__load_page_nearby()
        pattern_sc = re.compile('FM\.view\(({"ns":"pl\.content\.miniTab\.index","domid":"Pl_Core_Pt6Rank__39".*"})', re.DOTALL)
        for page in self.__pages_nearby:
            mo = pattern_sc.search(page)
            if mo is None:
                raise Exception("__load_page_nearby(): 页面中无正则表达式匹配信息。")
            js_text = json.loads(mo.group(1))
            content = js_text['html']
            soup = BeautifulSoup(content, 'lxml')
            tags = soup.select('div[class="title W_autocut"] a[class="S_txt1"]')
            for tag in tags:
                self.__urls_nearby.append(tag.attrs['href'])
        print('get_urls_from_page_nearby():________所有附近热门条目主页URL已抽取。________')

if __name__ == '__main__':
    b = BruceBanner()
    # b.get_page_nearby()
    b.get_urls_from_page_nearby()
