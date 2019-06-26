import _pickle as cPickle
from sklearn.externals import joblib
import os
import pandas as pd
import numpy as np
upper_loc=os.path.dirname(os.path.realpath(__file__))
FEATURE_DATAPATH =upper_loc+"/data/feature/feature_{START}_{END}_{TYPE}_{DETAIL}.sav" # for pickle file output(train/test)
raw_DATAPATH = upper_loc+"/data/crawling/raw_{START}_{END}_{FORMAT}"
url_DATAPAHT=upper_loc+"/data/crawling/url_{START}_{END}"
if __name__ == "__main__":
    print(upper_loc)


# url 데이터를 가져온다
'''
start: url 수집 시작 날짜
end: url 수집 종료 날짜
'''
def read_url(start,end):
    with open(url_DATAPAHT.format(START=start,END=end)+'.pkl',"rb") as infile:
        df=cPickle.load(infile)
    return df

#url 데이터를 저장한다
'''
res: url이 담겨 있는 list
start: url 수집 시작 날짜
end: url 수집 종료 날짜

ex> 
url_20180101_20181231.pkl
'''
def save_url(res,start,end):
    assert isinstance(res,list)

    with open(url_DATAPAHT.format(START=start,END=end)+'.pkl',"wb") as outfile:
        cPickle.dump(res,outfile,-1)
    with open(url_DATAPAHT.format(START=start,END=end)+'_ex.txt',"w") as outfile:
        outfile.write(str(res[:5]))
    return 

# 크롤링된 데이터를 가져온다
'''
start: url 수집 시작 날짜
end: url 수집 종료 날짜
format_: 댓글인 경우 com, 본문인 경우 atl 입력
'''
def read_raw(start,end,format_):
    infilepath=raw_DATAPATH.format(START=start,END=end,FORMAT=format_)
    df = joblib.load(infilepath+'.sav')
    return df

#크롤링된 데이터를 저장한다
'''
res: 크롤링한 dataframe 데이터
start: url 수집 시작 날짜
end: url 수집 종료 날짜
format_: 댓글인 경우 com, 본문인 경우 atl 입력

ex>
raw_20180101_20181231_com.sav
'''
def save_raw(res,start,end,format_):
    assert isinstance(res,pd.DataFrame)

    outfilepath=raw_DATAPATH.format(START=start,END=end,FORMAT=format_)
    joblib.dump(res,outfilepath+'.sav')
    with open(outfilepath+'_ex.txt',"w",encoding="utf-8") as outfile:

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            outfile.write('data length: {}\n header_list: {} \n'.format(res.shape[0],list(res.columns.values))+'\n'+'_'*40+'\n')
            outfile.write(str(res.head(5)))
    return 

#feature 데이터를 가져온다.
'''
start: url 수집 시작 날짜
end: url 수집 종료 날짜
type_: feature 특징
detail: 테스트 데이터는 test, 훈련 데이터는 train
'''
def read_feature(start,end,type_,detail):
    infile=FEATURE_DATAPATH.format(START=start,END=end,TYPE=type_,DETATIL=detail)
    df = joblib.load(infile)
    return df

#feature 데이터를 저장한다.
'''
res: feature을 가진 nparray 데이터
start: url 수집 시작 날짜
end: url 수집 종료 날짜
type_: feature 특징
detail: 테스트 데이터는 test, 훈련 데이터는 train

ex>
feature_20180101_20181231_tfidf_train.sav
'''
def save_feature(res,start,end,type_,detail):
    assert isinstance(res,np.array)
    outfile=FEATURE_DATAPATH.format(START=start,END=end,TYPE=type_,DETATIL=detail)
    joblib.dump(res,outfile)
    return 
