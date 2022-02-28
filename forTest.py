#-*- codeing = utf-8 -*-
from selenium import webdriver
import time
import json
import unittest


class ForTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wd = webdriver.Chrome('./chromedriver.exe')
        # 一次性获取网页内所有工作（limit限制个数，限制1000，最多抓取1000）
        self.wd.get('https://xskydata.jobs.feishu.cn/school/?current=1&limit=1000')
        # 设置休眠时间 让js渲染网页
        time.sleep(0.5)
        # 创建空列表装工作字典
        self.positionList = []

    def tearDown(self) -> None:
        self.wd.quit()

    def write_file(self, path, text):
        with open(path, "w") as file:
            json.dump(text, file, ensure_ascii=False, sort_keys=True, indent=4)

    def test_getData(self):
        # 创建工作字典
        positionDicts = {}
        # 工作标题
        positionTitles = self.wd.find_elements_by_class_name("positionItem-title-text")
        # 工作地点和类别
        positionPandC = self.wd.find_elements_by_class_name("positionItem-subTitle")
        # 工作职责
        positionDuties = self.wd.find_elements_by_class_name("positionItem-jobDesc")
        # 循环遍历工作，并添加进列表
        for i in range(len(positionTitles)):
            positionDicts["title"] = positionTitles[i].text
            positionDicts["place"] = positionPandC[i].text.split("\n")[0]
            positionDicts["category"] = positionPandC[i].text.split("\n")[1]
            positionDicts["duty"] = positionDuties[i].text
            self.positionList.append(positionDicts)
        self.write_file("./position.json", self.positionList)


if __name__ == '__main__':
    unittest.main()