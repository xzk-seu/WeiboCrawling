from LocationCode import LocationCode
from PageDown import PageDown
from Extractor import Extractor
import _CODE
from util.MyDataBase import MyDataBase
from util.MyWorksheet import MyWorksheet


class Spider:
    def __init__(self, interval=3):
        # 结果
        self.__posts = []

        self.__interval = interval

        self.__code_location = None

    def start(self):
        code = LocationCode()
        self.__code_location = code.code()
        # print(self.__code_location)

        down = PageDown()
        extractor = Extractor(interval=self.__interval)
        for item in self.__code_location.items():
            for index in range(1, 24):
                html = down.attack_home_page(code_item=item, index=index)
                if html is _CODE.ERROR_CODE:
                    break
                elif html is _CODE.NONE_CODE:
                    continue
                else:
                    self.__posts += extractor.extractor(html)
                if extractor.is_too_old():
                    break

            for i in range(1, 24):
                for j in range(0, 2):
                    html = down.attack_page_bar(code_item=item, i=i, j=j)
                    if html is _CODE.ERROR_CODE:
                        break
                    elif html is _CODE.NONE_CODE:
                        continue
                    else:
                        self.__posts += extractor.extractor(html)
                if extractor.is_too_old():
                    break

        self.__posts = list(set(self.__posts))

        db = MyDataBase()
        db.start()
        db.db_insert(self.__posts)
        db.close()

        ws = MyWorksheet()
        ws.save_worksheet(self.__posts)



