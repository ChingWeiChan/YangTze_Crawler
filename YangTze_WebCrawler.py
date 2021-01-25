# -*- coding: utf-8 -*-
"""
擷取:揚子高級中學網頁
@author: Chan Ching-Wei
"""
import requests
import re
import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import numpy as np

#Chinese fonts
plt.rcParams['font.family']=['Noto Sans CJK TC']

name = ["三版塊加總", "校園新鮮事", "訊息公告", "榮譽榜"]
total_Article = {}
total_Click = {}
area_Click = {"校園新鮮事": 0, "訊息公告": 0, "榮譽榜": 0}  # 迴圈變數k可作為判斷哪一區域的標準
area_Article = {"校園新鮮事": 0, "訊息公告": 0, "榮譽榜": 0}  # 迴圈變數k可作為判斷哪一區域的標準


def show_data(data, article, name):

    # Graph

    if name == "校園新鮮事":
        Magnification_start = 4000
        Magnification_end = 100000
        width_len = 70000
        dis = 4000
        plt.rc('xtick', labelsize=7)

    elif name == "訊息公告":
        Magnification_start = 4000
        Magnification_end = 100000
        width_len = 70000
        dis = 4000
        plt.rc('xtick', labelsize=7)

    elif name == "榮譽榜":
        Magnification_start = 2
        Magnification_end = 25
        width_len = 15
        dis = 2
        plt.rc('xtick', labelsize=10)
    elif name == "三各版塊":
        width_len = 0.25
        dis = 1/3
        plt.rc('xtick', labelsize=7)
    elif name == "三大版塊":
        Magnification_start = 4000
        Magnification_end = 100000
        width_len = 70000
        dis = 4000
        plt.rc('xtick', labelsize=7)

    int_list = []
    for i in data.keys():
        int_list.append(int(data[i]))
    if name == "三各版塊":
        start = 0.5
        end = 3
    else:
        start = len(list(data.values())) * Magnification_start  # 刻度設定
        end = len(list(data.values())) * Magnification_end  # 刻度設定
    xticks = np.linspace(start, end, len(list(data.values())))  # 設定x軸刻度範圍及座標
    plt.xticks(xticks, rotation=40)  # 設定x軸刻度範圍及座標 (Rotation:X軸座標的角度)
    plt.xlim(0, end+len(list(data.values()))*dis)
    if article == True:
        plt.ylim(0, int(max(int_list))+30)
        k = 2
        classification = "各處室文章總數"
        text_size = 8
    else:
        plt.ylim(0, int(max(int_list))+10000)  # 文章跟點閱率的範圍與大小設定
        if name == "三各版塊" or name == "三大版塊":
            k = 3000
        else:
            k = 470
        classification = "各處室網頁點閱總人數"
        text_size = 5
    if name == "三各版塊":
        classification += '之總和'

    plt.bar(xticks, int_list, align='center',
            tick_label=list(data.keys()), width=width_len)

    j = start
    plt.title("%s 揚子中學%s%s" % (time.strftime("%m/%d"), name, classification))
    for i in list(data.values()):
        plt.text(j, int(i)+k, i, horizontalalignment='center',
                 fontsize=text_size)
        j += float((end-start)/(len(list(data.values()))-1))
    plt.savefig("%s_%s%s.png" % (time.strftime("%m_%d"),
                                 name, classification), dpi=500, format="png")
    plt.close("all")


for k in range(1, 4):
    
    '''
    k = 1 : 校園新鮮事
    K = 2 : 訊息公告
    k = 3 : 榮譽榜
    '''
    print("start to crawl {}....".format(name[k]))
    i = 1  # from page one to crawl
    ClickDict = {}
    ArticleDict = {}
    while True:
        html = requests.get("http://www.ytjh.ylc.edu.tw/news/{}?page={}".format(k, i))
        html_bp = BeautifulSoup(html.text, 'html.parser')
        data1 = html_bp.select('.article-title')
        if data1 == []:
            break  # 爬到最後一頁
        print("Get unit & Click Rate...Page:{}".format(i))
        data_unit = html_bp.find_all(text=re.compile('單位 :'))  # 擷取單位文字
        data_ClickRate = html_bp.find_all(text=re.compile('點閱率'))  # 擷取點閱率文字
        for data in range(len(data1)):
            # print(data1[data].find('a').text)
            # print(data_unit[data])
            # print(data_ClickRate[data])
            # ArticleTitle.append(data1[data].find('a').text)  #目前標題非擷取重點
            Department = re.compile(r' 單位 : (.*)').search(data_unit[data]).group(1)
            if Department == '':
                continue  # 發現有單位為空白，不列入計算
            ClickRate = re.compile('\d+').search(data_ClickRate[data]).group()
            try:

                ClickDict[Department] = int(ClickRate)+int(ClickDict[Department])
                ArticleDict[Department] = int(ArticleDict[Department])+1

            except:

                ClickDict[Department] = ClickRate
                ArticleDict[Department] = 1

            try:
                total_Click[Department] = int(total_Click[Department])+int(ClickRate)
                total_Article[Department] = int(total_Article[Department])+1
            except:
                total_Click[Department] = ClickRate
                total_Article[Department] = 1

        i += 1
    print("end to crawl {}....".format(name[k]))
    for j in ClickDict.keys():
        area_Click["%s" % name[k]] = int(
            ClickDict[j])+int(area_Click["%s" % name[k]])
        area_Article["%s" % name[k]] = int(
            ArticleDict[j])+int(area_Article["%s" % name[k]])
        print("{} 觀看人數:{}   文章數量:{}".format(j, ClickDict[j], ArticleDict[j]))

    show_data(ClickDict, False, name[k])
    show_data(ArticleDict, True, name[k])


show_data(total_Click, False, name[0])
show_data(total_Article, True, name[0])
show_data(area_Click, False, "三各版塊")
show_data(area_Article, True, "三各版塊")
# show_data(ClickDict,False,name[3])
