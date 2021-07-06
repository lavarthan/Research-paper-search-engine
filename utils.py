import spacy
import pandas as pd
from rank_bm25 import BM25Okapi
from tqdm import tqdm
import ast
import time
import pickle

# load our data
df = pd.read_csv('train_data/preprocessed.csv')

# load our model
with open('model/model.pkl', 'rb') as file:
    model = pickle.load(file)


def get_number_of_docs(tokenized_query):
    doc_scores = model.get_scores(tokenized_query)
    doc_scores.sort()
    doc_scores = doc_scores[::-1]
    return sum(i > 5.0 for i in doc_scores)


def get_search_index(query):
    tokenized_query = query.lower().split(" ")
    doc_scores = model.get_scores(tokenized_query)

    t0 = time.time()
    n = get_number_of_docs(tokenized_query)
    results = model.get_top_n(tokenized_query, df.train_data.values, n=n)
    t1 = time.time()
    print(f'Searched 28,376 records in {round(t1 - t0, 3)} seconds \n')
    timing = f'Searched 28,376 records in {round(t1 - t0, 3)} seconds \n'
    indexes = []
    for result in results:
        ind = df.loc[df['train_data'] == result].index[0]
        print()
        indexes.append(ind)
    return indexes,timing


def make_dic(data):
    temp_data = [_.split(' => ') for _ in ast.literal_eval(data)]
    final = {}
    for i in temp_data:
        if len(i) == 2:
            final[i[0]] = i[1]
        else:
            final[i[0]] = ''
    return final


def get_data(indexes):
    data = []
    for i in indexes:
        dic = {'title': df['Title'][i],
               'link': df['Link'][i],
               'authors': make_dic(df['Authors'][i]),
               'date': df['Published date'][i]}
        data.append(dic)
    return data
