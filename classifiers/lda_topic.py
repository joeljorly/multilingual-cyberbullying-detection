# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from gensim.models import CoherenceModel

import numpy as np

file=open("pre_out.txt","r").readlines()
y=[]
documents=[]
for i in file:
    documents.append(i[:-1])
print(documents)

texts = [[word for word in document.lower().split()] for document in documents]
print(texts)

all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) ==1)
print(tokens_once)

texts = [[word for word in text if word not in tokens_once]
         for text in texts]

print(texts)

dictionary = corpora.Dictionary(texts)

print(dictionary)

print(dictionary.token2id)

new_doc = "poda tholvi"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)

corpus = [dictionary.doc2bow(text) for text in texts]

import numpy
tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus] 
print(corpus_tfidf)

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) 
print(lsi)

corpus_lsi = lsi[corpus_tfidf]
print(corpus_lsi)
topic = lsi.print_topics(2)
print(topic)

lsi.save('model.lsi') 

lsi = models.LsiModel.load('model.lsi')
print(lsi)

doc = "tholvi myre"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
print(vec_lsi)

bow_doc_4310 = corpus[58]
for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0],dictionary[bow_doc_4310[i][0]],bow_doc_4310[i][1]))

res=dictionary.token2id.keys()
#print(res)

from sklearn.feature_extraction.text import TfidfVectorizer
bow_vectorizer = TfidfVectorizer()
bow = bow_vectorizer.fit_transform(res).toarray()
#term_doc_mat=bow_vectorizer.transform(res)



def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
            result.append(token)
    return result

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=5,
                                           alpha='auto',
                                           )
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

unseen_document = 'nee poda myre'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))

coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)
