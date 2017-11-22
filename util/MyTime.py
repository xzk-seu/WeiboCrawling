"""_time"""
import datetime


# 封装时间操作
class MyTime:

    # 返回时间间隔
    @ staticmethod
    def interval(weibo_time):
        now_time = datetime.datetime.now()
        year = weibo_time[:4]
        month = weibo_time[5:7]
        day = weibo_time[8:10]

        early_time = datetime.datetime(int(year), int(month), int(day),)
        return (now_time - early_time).days


if __name__ == '__main__':
    print(MyTime.interval('2017-11-20'))
