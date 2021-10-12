# 爬取杨凌自2011年10月的天气并渲染网页与图片

'''
# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/11 21:24
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : tianqi.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from pyecharts.charts import Line,Page
import pyecharts.options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot



url = 'http://www.tianqihoubao.com/lishi/yangling/month/'

def ask_url(url):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe bKit/537.36 (KHTML, like Gecko) Chrome/93.0.4544.0 Safari/537.36 Edg/93.0.933.1",
        }  # 头部信息用户代理
    try:
        html = requests.get(url,headers=headers).text
    except Exception as err:
        print(err)
        html=err
    return html



def analyze_html(url):
    datalist = []
    html =ask_url(url)
    soup = BeautifulSoup(html, "lxml")
    for item in soup.find_all('table', class_="b"):
        item  = str(item)
        datalist.append(item.replace(' ','').replace('\n','').replace('\r',''))
    weatherlist = datalist[0].split('</tr>')
    weatherlist.pop(0)
    weatherlist.pop(len(weatherlist)-1)
    return weatherlist

def draw(url):
    list=analyze_html(url)
    temp_dic={}
    # 日期
    date_list=[]
    # 白天温度
    temp_day=[]
    # 夜晚温度
    temp_night=[]
    for item in list:
        find_temp=re.compile('[\u4e00-\u9fa5]</td><td>(.*?)℃</td><td>')
        find_date=re.compile('[\u4e00-\u9fa5]">(.*?)日</a>')
        find_year=re.compile('[\u4e00-\u9fa5]">(.*?)月')
        date=re.findall(find_date,item)
        temp=re.findall(find_temp,item)
        year=re.findall(find_year,item)[0]
        temp_dic[date[0]]=temp[0].replace('℃','')
        date_list.append(date[0])
        temp_sum=temp[0].replace('℃','').split('/')
        #有些数据不全，没有白天的温度或者晚上的温度
        if temp_sum[0]=='':
            print('0空')
        else:
            temp_day.append(int(temp_sum[0]))
        if temp_sum[1]=='':
            print('1空')
        else:
            temp_night.append(int(temp_sum[1]))
    #24H温度列表
    all_temp=(temp_day+temp_night)
    print(all_temp)
    #最高温
    max_temp=int(max(all_temp))
    #最低温
    min_temp=int(min(all_temp))

    # print(temp_dic)
    # print(temp_day)
    # print(len(temp_day))

    # 绘图
    line1=(
        Line(init_opts=opts.InitOpts(bg_color='#ffffff')) # 生成line类型图表
        .add_xaxis(date_list)
        .add_yaxis('白天',temp_day,is_smooth=True,
                   markline_opts=opts.MarkLineOpts(
                       data=[

                           opts.MarkLineItem(symbol="none", x="90%", y="max"),
                           opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                       ]
                   ),
                   )
        .add_yaxis('夜晚',temp_night,is_smooth=True,
                   markline_opts=opts.MarkLineOpts(
                       data=[
                           opts.MarkLineItem(type_="min", name="最低点"),
                           opts.MarkLineItem(symbol="none", x="90%", y="max"),
                       ]
                   ),
                   )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_right=0),
            title_opts=opts.TitleOpts(title='%s月温度情况'%year,subtitle='24H最高温度%s℃,最低温度%s℃\n部分数据存在空值'%(max_temp,min_temp),pos_left='center',),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
                name="日期",
            ),
            yaxis_opts=opts.AxisOpts(name="温度(℃)"),
        )
    )
    return line1
    # line1.render('pyecharts-line.html') # 生成网页文件
    # make_snapshot(snapshot, line1.render(), "%s.png"%year) #渲染图片

if __name__ == '__main__':
    from time import time
    start = time()
    page = Page()
    for i in range(11):
        askurl=url+str(2010+i+1)+'10.html'
        print(askurl)
        line=draw(askurl)
        page.add(line)
    page.render("test.html")
    end = time()
    print('Cost {} seconds'.format((end - start) / 5))


'''
