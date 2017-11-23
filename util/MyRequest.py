"""url request module"""

import user.Agents
import user.Cookies
import random
import requests
import time


class MyRequest(object):
    def __init__(self):
        self.__user_agents = user.Agents.agents
        self.__cookies = user.Cookies.cookies
        self.__headers = {
            'User_Agent': self.__user_agents[0],
            'cookie': self.__cookies[0]
        }

    def __refresh_headers(self):
        self.__headers['User_Agent'] = random.choice(self.__user_agents)
        self.__headers['cookie'] = random.choice(self.__cookies)

    # 根据URL返回内容
    def __get_page_content(self, url):
        r = requests.get(url=url, headers=self.__headers)
        r.encoding = 'utf-8'
        self.__refresh_headers()
        time.sleep(random.choice(range(3, 7, 2)))
        # time.sleep(random.choice(range(9, 15, 3)))
        return r.text

    def content(self, url):
        return self.__get_page_content(url)


