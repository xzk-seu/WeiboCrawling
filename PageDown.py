import json
import logging
import os
import re

import _CODE
from res.URLs import urls_model
from util.MyRequest import MyRequest


logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.getcwd(), 'logs', 'PageDown.txt'),
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program.')

""" 
Down模块：

    1. 提取主页面

        
    2. 提取动态页    
        
"""


class PageDown:
    def __init__(self):
        # print("Class:PageDown")
        self.__request = MyRequest()
        self.__path_home = os.path.join(os.getcwd(), 'data', 'pages_home')
        self.__path_bar = os.path.join(os.getcwd(), 'data', 'pages_bar')

    # 将地区的主页包含的HTML记录下来,注意！ 是一个页面
    # 输入地区码字典item，页面索引，输出html页面内容
    def attack_home_page(self, code_item, index):
        page_name = code_item[0] + 'Home_' + str(index) + '.txt'

        # 用于提取源代码中script标签下的JSON信息所用的正则表达式
        pattern = re.compile(
            "FM\.view\(({\"ns\":\"pl\.content\.homeFeed\.index\",\"domid\":\"Pl_Core_MixedFeed__35\",.*)\)</script>")

        content = self.__request.content(urls_model['Home'].format(code_location=code_item[1], page=index))
        mo = pattern.search(content)

        if mo is not None:
            js_text = mo.group(1)
        else:
            return _CODE.NONE_CODE

        if 'html' not in json.loads(js_text).keys():
            return _CODE.NONE_CODE
        html = json.loads(js_text)['html']

        length = len(html)
        # 如果页面中没有过多内容，则不写入html
        if length < 800:
            return _CODE.NONE_CODE
        else:
            with open(os.path.join(self.__path_home, page_name), 'w', encoding='utf-8') as f:
                f.write(html)
        print("attack_home_page():_____已读取", code_item[0], str(index), "的内容。_____")
        return html

    # 将动态页面的html记录下来
    def attack_page_bar(self, code_item, i, j):
        page_name = code_item[0] + 'Bar_' + str(i) + '.' + str(j) + '.txt'

        content = self.__request.content(urls_model['JS'].format(page=i, pre_page=i, pagebar=j,
                                                                 current_page=(i * 3 - 2 + j),
                                                                 code_location=code_item[1]))
        # if 'html' not in json.loads(content).keys():
        #     return _CODE.NONE_CODE
        html = json.loads(content)['data']
        length = len(html)

        # 如果页面中没有过多内容，则不写入html
        if 400 < length < 1000:
            return _CODE.NONE_CODE
        # 如果页面为空，跳过此地区
        elif length <= 400:
            return _CODE.ERROR_CODE
        else:
            with open(os.path.join(self.__path_bar, page_name), 'w', encoding='utf-8') as f:
                f.write(html)
        print("attack_page_bar():_____已读取", code_item[0], str(i), str(j), "的内容。_____")
        return html



