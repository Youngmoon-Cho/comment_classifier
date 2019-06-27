from bs4 import BeautifulSoup
import requests
import re

import pandas as pd
import numpy as np

import os
import sys
import _pickle as cPickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from fileio import *

import time


# 코딩 시간 측정
start = time.time()


# 제목을 추출하는 함수
def news_title(URL):
    html = requests.get(URL).text
    parsed_data = BeautifulSoup(html, 'html.parser')

    news_title = parsed_data.find('title')
    return news_title.text[0:-9]


# 날짜를 추출하는 함수
def news_date(URL):
    html = requests.get(URL).text
    parsed_data = BeautifulSoup(html, 'html.parser')

    news_date = parsed_data.find('em')
    return news_date.text


# 기사 본문을 추출하는 함수
def news_contents(URL):
    html = requests.get(URL).text
    parsed_data = BeautifulSoup(html, 'html.parser')

    text = ''
    for item in parsed_data.find_all('div', id='realArtcContents'):
        text = text + str(item.find_all(text=True))
    return text[65:]


# url 데이터를 가져온다. datas[]로 원하는 url 숫자 조정
with open('url_20180101_20181231.pkl', 'rb') as fin:
    datas = cPickle.load(fin)

url_list = datas[(50*304):(50*334)]


# 제목, 날짜, 본문 데이터를 추출한다
URL = 'https:'
titlelist = []
datelist = []
contentslist = []

for i in url_list:
    URL = URL + i

    titlelist.append(news_title(URL))
    datelist.append(news_date(URL))
    contentslist.append(news_contents(URL))

    URL = 'https:'

data = {'title' : titlelist, 'date' : datelist, 'contents' : contentslist}

frame = pd.DataFrame(data)


'''
res: 크롤링한 dataframe 데이터
start: url 수집 시작 날짜
end: url 수집 종료 날짜
format_: 댓글인 경우 com, 본문인 경우 atl 입력

ex>
raw_20180101_20181231_com.sav
'''
#크롤링된 데이터를 저장하는 함수
def save_raw(res,start,end,format_):
    assert isinstance(res,pd.DataFrame)

    outfilepath=raw_DATAPATH.format(START=start,END=end,FORMAT=format_)
    joblib.dump(res,outfilepath+'.sav')
    with open(outfilepath+'_ex.txt',"w",encoding="utf-8") as outfile:

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            outfile.write('data length: {}\n header_list: {} \n'.format(res.shape[0],list(res.columns.values))+'\n'+'_'*40+'\n')
            outfile.write(str(res.head(5)))
    return 


# 크롤링된 데이터를 저장한다
start = 20180101
end = 20180131
save_raw(frame,start,end,atl)


# 컴파일 완료 확인 및 소요시간 측정
print("The End!")
print("time :", time.time() - start)