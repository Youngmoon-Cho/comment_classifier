import _pickle as cPickle
from sklearn.externals import joblib
import os

upper_loc=os.path.dirname(os.path.realpath(__file__))
FEATURE_DATAPATH =upper_loc+"/data/feature/feature_{START}_{END}_{TYPE}_{DETAIL}.sav" # for pickle file output(train/test)
raw_DATAPATH = upper_loc+"data/crawling/url_{START}_{END}_{FORMAT}"
url_DATAPAHT=upper_loc+"/data/crawling/url_{START}_{END}"

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
'''
def save_url(res,start,end):
    with open(url_DATAPAHT.format(START=start,END=end)+'.pkl',"wb") as outfile:
        cPickle.dump(res,outfile,-1)
    try:
        with open(url_DATAPAHT.format(START=start,END=end)+'_ex.txt',"w") as outfile:
            outfile.write(str(res[:5]))
    except:
        pass
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
'''
def save_raw(res,start,end,format_):
    outfilepath=raw_DATAPATH.format(START=start,END=end,FORMAT=format_)
    joblib.dump(res,outfilepath+'.sav')
    try:
        with open(outfilepath+'_ex.txt') as outfile:
            outfile.write(str(res.head(5)))
    except:
        pass
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
'''
def save_feature(res,start,end,type_,detail):
    outfile=FEATURE_DATAPATH.format(START=start,END=end,TYPE=type_,DETATIL=detail)
    joblib.dump(res,outfile)
    return 
