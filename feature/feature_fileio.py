import _pickle as cPickle
from sklearn.externals import joblib
import os

upper_loc=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FEATURE_DATAPATH =upper_loc+"/data/crawaling_{START}_{END}_{TYPE}.sav" # for pickle file output(train/test)
raw_DATAPATH = upper_loc+"data/crawling/url_{START}_{END}.pkl"

# 크롤링된 데이터를 가져온다
def read_raw(start,end):
    with open(raw_DATAPATH.format(START=start,END=end),'rb') as infile:
        df = cPickle.load(infile)
    return df

#feature 데이터를 가져온다.
def read_feature(start,end,type_):
    infile=FEATURE_DATAPATH.format(START=start,END=end,TYPE=type_)
    df = joblib.load(infile)
    return df
#feature 데이터를 저장한다.
def save_feature(res,start,end,type_):
    outfile=FEATURE_DATAPATH.format(START=start,END=end,TYPE=type_)
    df = joblib.dump(res,outfile)
    return df
