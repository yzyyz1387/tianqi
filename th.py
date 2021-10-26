# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/26 12:36
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : th.py
# @Software: PyCharm
import threading
import time
import tianqi
from pyecharts.charts import Line,Page
def single_th():
    for url in tianqi.urls:
        line=tianqi.draw(url)



def multi_th():
    ths=[]
    for url in tianqi.urls:
        ths.append(threading.Thread(target=tianqi.draw,args=(url,)))
    for th in ths:
        th.start()
    for th in ths:
        th.join()


if __name__ == '__main__':
    # start = time.time()
    # single_th()
    # end = time.time()
    # print('Cost {} seconds'.format((end - start) / 5))

    start = time.time()
    multi_th()
    end = time.time()
    print('Cost {} seconds'.format((end - start) / 5))