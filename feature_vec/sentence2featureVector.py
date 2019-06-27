# sentences_char_form = # 단어로 쪼개진 문장 데이터. sentences_char_form[i] = ["단어1","단어2",'단어3'] 꼴을 기대.
# one_hot_ylaebl = # label data from like/dislike ratio (one-hot encoded)

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import numpy as np


# 전체 단어를 다 모아서 뉴럴넷 모델의 인풋 데이터가 될 것.
def generate_sentences_image_2D(sentences_char_form, max_len_of_comment = 35):
    ''' 
    input 'sentences_char_form' is assumed to be written in nested list form.
    This funciton returns One-Hot encoded sentences image (2D ndarray for each sample)
    
    '''
    #  ref) 1. unseen label leads error
    
    ###########----OVERVIEW END----###########
    
    total_char_set = set(sum(sentences_char_form,[])) # erase duplicated char. All characters in input data
    total_char_list = list(total_char_set) 

    L_encoder = LabelEncoder()  # char -> label(number) encoder object
    L_encoder.fit(total_char_list) # set id for every char
    
    total_Label_list = L_encoder.transform(total_char_list) 
    total_Label_list = total_Label_list.reshape((len(total_Label_list),1))    # reshaped to fit OH_encoder below.
    print(f'The total number of character categories : {len(total_Label_list)}')
    
    OH_encoder = OneHotEncoder(sparse=False)
    OH_encoder.fit(total_Label_list) # set basis one-hot vector for each Label.
    
    sentences_image_2D = np.zeros((len(sentences_char_form),max_len_of_comment ,len(total_char_list)))    # this will contatin all sentence images
    
    for indx , sentence in enumerate(sentences_char_form):
        
        sentence2char_Label = L_encoder.transform(sentence) 
        Labeled_col_vec = sentence2char_Label.reshape((len(sentence2char_Label),1))  # make labeled col vec.
        OH_sentence = OH_encoder.transform(Labeled_col_vec)  # to one-hot encoded 2D array for each sentence
        
        # short comments -> add zeors // long comments -> cut tails
        if OH_sentence.shape[0] < max_len_of_comment: # append zeros for small comments
            add_zeros = np.zeros((max_len_of_comment-OH_sentence.shape[0] , OH_sentence.shape[1]))
            OH_sentence = np.concatenate((OH_sentence,add_zeros),axis=0)    # add zeros for short comment

        elif OH_sentence.shape[0] > max_len_of_comment: # cut large comments
            OH_sentence = OH_sentence[:max_len_of_comment, :]
        
        sentences_image_2D[indx] = OH_sentence    # merge OH sentences together
    
    return sentences_image_2D   # shape = (num of samples, len of comment, num of total chars)

