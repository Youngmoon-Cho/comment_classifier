from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

#인기 뉴스 태그
core_url="https://news.nate.com/rank/interest?sc=all&p=day&date={}"
#날짜 generator: 2018년 전체 조사
#note: type(dt_list)!=list
START='20180101'
END='20181231'
dt_list = pd.date_range(start=START, end=END).strftime("%Y%m%d")

'''
def url_test(URL):
    rough_data=requests.get(url=URL).text
    with open("url_collector_sample.txt","w") as outfile:
        outfile.write(rough_data)
'''
from bs4 import BeautifulSoup
def test_url_extractor(URL):
    url_list=list()
    html=requests.get(url=URL).text
    parsed_data=BeautifulSoup(html,'html.parser')
    #top1~5 parser
    #<div class="mlt01"> \n   <a href=
    top_urls=parsed_data.find_all('div',attrs={'class':'mlt01'})
    for i in top_urls:
        url_list.append(i.find('a')['href'])
    #top6~50 parser
    #mduRank rank[6-50]
    row_ruls=parsed_data.find('div',attrs={'id':'postRankSubject'}).find_all('a')
    for i in row_ruls:
        url_list.append(i['href'])
    
    return url_list


import os
import _pickle as cPickle
def main():
    upper_loc=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    url_list=[]
    for i in dt_list:
        url_list.extend(test_url_extractor(core_url.format(i)))
    with open(upper_loc+"/data/crawling/url_{start}_{end}.pkl".format(start=START,end=END),"wb") as outfile:
        cPickle.dump(url_list,outfile,-1)
    with open(upper_loc+"/data/crawling/url_{start}_{end}_ex.txt".format(start=START,end=END),"w") as outfile:
        outfile.write(str(url_list[:5]))

if __name__=="__main__":
    main()