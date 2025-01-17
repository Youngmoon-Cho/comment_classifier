from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

#url format
comment_url="https://comm.news.nate.com/Comment/ArticleComment/List?artc_sq={DATE}&order=&cmtr_fl=0&prebest=0&clean_idx=&user_nm=&fold=&mid={SEC}&domain=&argList=0&best=1&return_sq=&connectAuth=N{PP}"
page_url="&page={P}#comment"
#날짜 generator: 2018년 전체 조사
#note: type(dt_list)!=list
START='20180101'
END='20181231'
dt_list = pd.date_range(start=START, end=END).strftime("%Y%m%d")
del_url_file=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/crawling/error_url_{start}_{end}.txt".format(start=START,end=END)
error_cnt=0

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from fileio import read_url, save_raw
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
'''
URL: url 값
i: url을 대표하는 숫자, url list에서 i번째(0부터 시작) url에서 뽑아온 댓글에 i태그를 붙인다.
'''

def comment_extractor(URL,com_id):
    # 각 url당 100개의 댓글 수집(좋아요/싫어요 수의 편중 방지)
    df=pd.DataFrame(columns=['comment','like','dislike','date','id'])
    # 주어진 url을 comment_url로 변환
    comment_inf=re.split(r"/|[?]|=",URL)
    date,section=comment_inf[-3],comment_inf[-1]
    real_url=comment_url.format(DATE=date,SEC=section,PP=page_url)
    # 댓글 개수 확인/수집은 50개 이하로 수행
    #첫번째 페이지에 나온 댓글 제외: 베스트 댓글을 수집하기 때문에 삭제:23개
    html=requests.get(url=real_url.format(P=1),verify=False).text
    parsed_data=BeautifulSoup(html,'html.parser')
    try:
        num_com=int(parsed_data.find('a',attrs={'id':'tab_cmt'}).find('strong').contents[0])
    except: # if the article has been deleted, return empty dataframe file
        global error_cnt
        error_cnt+=1
        if com_id==0:#
            with open(del_url_file,'w') as outfile:
                outfile.write("\n")
                outfile.write(URL)
                outfile.write("\n0")
        else:
            with open(del_url_file,'a') as outfile:
                outfile.write("\n")
                outfile.write(URL)
                outfile.write("\n")
                outfile.write(str(com_id))
        return df
    # 댓글/좋아요/싫어요/작성 날짜
    cnt=0 #댓글 개수
    page=0 #페이지 수
    #regular expression/string for passinig
    comm_ox_id="cmt_{}_cnt_{}"
    df=pd.DataFrame(columns=['comment','like','dislike','date','id'])
    com_re=re.compile("<a\s")

    while cnt<=min(num_com,100):
        page+=1
        html=requests.get(url=real_url.format(P=page),verify=False).text
        #comment_raw: comment에 대한 모든 정보가 여기에 적혀 있음: 댓글/좋아요/싫어요/작성 날짜
        comment_raw=parsed_data.find('div',attrs={"class":"cmt_list"}).find_all('dl',attrs={"class":["cmt_item f_line","cmt_item"]})
        cnt+=sum(1 for _ in comment_raw)
        #parsing
        for i in comment_raw:
            try:#if crawling fails, immediately give up and do the next thing
                #date crawling
                com_date=i.find('span',attrs={"class":"date"}).contents[1]
                #like/dislike
                comm_id=i['id'].split('_')[-1]
                com_like=locale.atoi(i.find('strong',attrs={"id":comm_ox_id.format("o",comm_id)}).contents[0])
                com_dislike=locale.atoi(i.find('strong',attrs={"id":comm_ox_id.format("x",comm_id)}).contents[0])
                #comment
                com_raw=i.find('dd',attrs={"class":"usertxt"})
            except:
                continue
            try:#comment written on PC may not have img tag
                com_raw.find('img').extract()
            except:
                pass
            com_raw1= ''.join([str(item) for item in com_raw.contents])
            com_com=com_raw1[:com_re.search(com_raw1).start()]
            df.loc[len(df)]=[com_com,com_like,com_dislike,com_date,com_id]
    return df

def test(URL,i):
    comment_inf=re.split(r"/|[?]|=",URL)
    date,section=comment_inf[-3],comment_inf[-1]
    real_url=comment_url.format(DATE=date,SEC=section,PP=page_url)
    # 댓글 개수 확인/수집은 50개 이하로 수행
    #첫번째 페이지에 나온 댓글 제외: 베스트 댓글을 수집하기 때문에 삭제:23개
    html=requests.get(url=real_url.format(P=1),verify=False).text
    parsed_data=BeautifulSoup(html,'html.parser')
    try:
        num_com=int(parsed_data.find('a',attrs={'id':'tab_cmt'}).find('strong').contents[0])-23
    except:
        print(URL)
        print(i)

#mpi_test:
from mpi4py import MPI
'''
def mpi_test:
    size=MPI.COMM_WOLD.get
'''
def main_test():
    url_list=read_url(START,END)
    for i,URL in enumerate(url_list):
        test(URL,i)


import sys
sys.setrecursionlimit(130000)
def main():
    url_list=read_url(START,END)
    df=pd.DataFrame(columns=['comment','like','dislike','date','id'])
    file_cnt=0
    iter_cnt=0
    file_form="com_{}_mpi"
    #MPI START
    COMM=MPI.COMM_WORLD
    SIZE=COMM.Get_size()
    if SIZE==1:
        for i,URL in enumerate(url_list):
            iter_cnt+=1
            new_df=comment_extractor(URL,i)
            df=df.append(new_df)
            if iter_cnt>=2500:
                iter_cnt=0
                save_raw(df,START,END,file_form.format(file_cnt))
                file_cnt+=1
                df=pd.DataFrame(columns=['comment','like','dislike','date','id'])
        
        save_raw(df,START,END,file_form.format(file_cnt))
    else:#master and slave
        #loc: location of url, url: real_url
        #sen files
        RANK=COMM.Get_rank()
        if RANK==0:
            for i in range(1,SIZE):
                COMM.send([url_list.pop(0),i],dest=i)
            loc=SIZE
        else:
            RECVMSG=COMM.recv(source=0)
        #master: control flow and storing,notice to programmer
        #slave: url_extraction
        while url_list:
            if RANK==0:
                for i in range(1,SIZE):
                    iter_cnt+=1
                    RECVMSG=COMM.recv(source=i)
                    #dataframefile receving!
                    if url_list:
                        COMM.send([url_list.pop(0),loc],dest=i)
                        loc+=1
                    df=df.append(RECVMSG)
                    if iter_cnt>1000:
                        iter_cnt=0
                        save_raw(df,START,END,file_form.format(file_cnt))
                        file_cnt+=1
                        df=pd.DataFrame(columns=['comment','like','dislike','date','id'])
                    if not url_list:#url_list is empty
                        break
                    if iter_cnt%100==99:
                        print("url: {}\ncnt: {}".format(url_list[0],loc))
            else:
                #sendmsg: dataframe
                SENDMSG=comment_extractor(RECVMSG[0],RECVMSG[1])
                COMM.send(SENDMSG,dest=0)
                RECVMSG=COMM.recv(source=0)
    
    with open(del_url_file,'r+') as outfile:
            outfile.seek(0)
            outfile.write("num of error url: ")
            outfile.write(str(error_cnt))




if __name__=="__main__":
    main()