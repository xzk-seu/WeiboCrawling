import user.Agents
import user.Cookies
import random
import requests
import os
import time
from dict.URLs import urls_dengfeng


class Avengers(object):
    def __init__(self):
        self.__user_agents = user.Agents.agents
        self.__cookies = user.Cookies.cookies
        self.__headers = {
            'User_Agent': self.__user_agents[0],
            'cookie': self.__cookies[0]
        }
        self.urls = urls_dengfeng
        self.max_page_num = {
            'dengfeng': 23
        }
        self.html = []
        self.path_html = r'./data/html'
        self.html_index = 0
        self.path_work_sheet = ''

    def __refresh_headers(self):
        self.__headers['User_Agent'] = random.choice(self.__user_agents)
        self.__headers['cookie'] = random.choice(self.__cookies)

    def get_html_index(self):
        list_html = os.listdir(self.path_html)
        self.html_index = len(list_html)

    # 根据URL返回内容
    def get_page(self, url):
        r = requests.get(url=url, headers=self.__headers)
        r.encoding = 'utf-8'
        self.__refresh_headers()
        time.sleep(random.choice(range(3, 7, 2)))
        return r.text
