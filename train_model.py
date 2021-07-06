import spacy
import pandas as pd
from rank_bm25 import BM25Okapi
from tqdm import tqdm
import ast
import pickle

# load our data
df = pd.read_csv('train_data/final.csv')


# pre process the data
def preprocess(authors, title):
    li = ast.literal_eval(authors)
    authors_text = ', '.join([_.split(' => ')[0] for _ in li])
    final = title + ' by ' + authors_text
    return final


# save preprocess data
for i in range(df.shape[0]):
    print(i, end=',')
    df['train_data'][i] = preprocess(df['Authors'][i], df['Title'][i])

# load our data
df = pd.to_csv('train_data/preprocessed.csv')

# train model
nlp = spacy.load("en_core_web_sm")
text_list = df.train_data.str.lower().values

# for our tokenized corpus
tok_text = []

# Tokenizing using SpaCy:
for doc in tqdm(nlp.pipe(text_list, disable=["tagger", "parser", "ner"])):
    tok = [t.text for t in doc if t.is_alpha]
    tok_text.append(tok)

# train our model
bm25 = BM25Okapi(tok_text)

# save model
Pkl_Filename = "model.pkl"
with open(Pkl_Filename, 'wb') as file:
    pickle.dump(bm25, file)
