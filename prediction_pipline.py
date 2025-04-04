import numpy as np
import pandas as pd
import re
import string
import pickle

#create PorterStemmer object
from nltk.stem import PorterStemmer
ps = PorterStemmer()

#load the model
with open('static/model/model.pickle','rb') as f:
    model=pickle.load(f)

#load stopwords
with open('static/model/corpora/stopwords/english','r') as file:
    sw = file.read().splitlines()

#load vocabulary
vocab = pd.read_csv('static/model/vocabulary.txt', header=None)
tokens = vocab[0].tolist()

#remove unnessary data
def remove_symbols(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def preprocessing(text):
    data = pd.DataFrame([text],columns=['tweet'])
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(x.lower() for x in x.split()))
    data["tweet"] = data['tweet'].apply(lambda x: " ".join(re.sub(r'^https?:\/\/.*[\r\n]*', '',x,flags=re.MULTILINE)for x in x.split()))
    data["tweet"]=data["tweet"].apply(remove_symbols)
    data["tweet"]= data['tweet'].str.replace('\d+','',regex=True)
    data["tweet"] = data["tweet"].apply(lambda x: " ".join([word for word in x.split() if word not in sw]))
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(ps.stem(x) for x in x.split()))
    return data["tweet"]

def vectorizer(ds):
    vectorized_lst = []
    for sentence in ds:
        sentence_lst = np.zeros(len(tokens))

        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_lst[i] = 1
        vectorized_lst.append(sentence_lst)
    vectorized_list_new = np.asarray(vectorized_lst,dtype=np.float32)

    return vectorized_list_new

#get prediction
def get_Prediction(vectorized_text):
    prediction = model.predict(vectorized_text)
    if prediction ==1:
        return 'negative'
    else:
        return 'postive'