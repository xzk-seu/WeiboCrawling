"""code()"""
import json
import logging
import os
import re
import time

from bs4 import BeautifulSoup

from res.URLs import urls_model
from util.MyRequest import MyRequest


# 提取所有需要的地区码
class LocationCode:

    def __init__(self):
        # print("Class:LocationCode")
        self.__request = MyRequest()
        # 地区码保存文件
        self.__path_location_code = os.path.join(os.getcwd(), 'res', 'location_code.txt')
        self.__location_code = {
            '登封': '1001018008641018500000000',
        }

        self.__path_nearby = os.path.join(os.getcwd(), 'data', 'pages_nearby')
        self.__pages_nearby = []

    # 将附近热门页面源码下载
    def __get_page_nearby(self):
        page_name = 'nearby_{num}.txt'

        for i in range(1, 11):
            content = self.__request.content(urls_model['Nearby'].format(page=i))
            # logging.debug('get_page_nearby(): The len of content is ' + str(len(content)))

            # 如果文件大小不符合要求，则进行迭代，如果迭代次数超过五次都未满足要求，不再读取该页面。
            iterator = 0
            if len(content) < 58000 and iterator < 5:
                content = self.__request.content(urls_model['Nearby'].format(page=i))
                iterator += 1
            if len(content) > 58000:
                with open(os.path.join(self.__path_nearby, page_name.format(num=i)), 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                logging.debug('get_page_nearby():第个文件' + str(i) + '写入失败。')
            time.sleep(10)
        print('get_page_nearby():________Done!________')

    def __load_page_nearby(self):
        print('__load_page_nearby():________start________')
        list_page = os.listdir(self.__path_nearby)
        for page_name in list_page:
            with open(os.path.join(self.__path_nearby, page_name), 'r', encoding='utf-8') as f:
                self.__pages_nearby.append(f.read())

    def __get_code_location_nearby(self):
        if len(self.__pages_nearby) is 0:
            self.__load_page_nearby()
        if len(self.__pages_nearby) is 0:
            self.__get_page_nearby()
            self.__load_page_nearby()

        pattern_script = re.compile('FM\.view\(({"ns":"pl\.content\.miniTab\.index","domid":"Pl_Core_Pt6Rank__39".*"})',
                                    re.DOTALL)
        pattern_code = re.compile('/p/([A-Za-z0-9]*)')

        f = open(self.__path_location_code, 'w' , encoding='utf-8')
        for page in self.__pages_nearby:
            mo = pattern_script.search(page)
            if mo is None:
                raise Exception("__load_page_nearby(): 页面中无与正则表达式匹配的JSON信息。")
            js_text = json.loads(mo.group(1))
            content = js_text['html']
            soup = BeautifulSoup(content, 'lxml')
            tags = soup.select('div[class="title W_autocut"] a[class="S_txt1"]')

            for tag in tags:
                # self.__urls_nearby.append(tag.attrs['href'])
                mo = pattern_code.search(tag.attrs['href'])
                if mo is None:
                    continue
                else:
                    self.__location_code[tag.text] = mo.group(1)
                    f.write(tag.text + ' ')
                    f.write(mo.group(1) + '\n')
        f.close()
        print('get_urls_from_page_nearby():________所有附近热门条目主页Code已抽取。________')

    def code(self):
        with open(self.__path_location_code, 'r', encoding='utf-8') as f:
            if f.read() is None:
                for line in f.readlines():
                    item = line.strip().split()
                    self.__location_code[item[0]] = item[1]
                return self.__location_code

        self.__get_code_location_nearby()
        return self.__location_code


if __name__ == '__main__':
    l = LocationCode()
    print(l.code())
