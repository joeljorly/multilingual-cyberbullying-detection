# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
import numpy as np
import pickle

label=[]
comm=[]
b=[]
s=[]
input=open("input.txt","r").readlines()
support=open("support.txt","r").read()
bully=open("bully.txt","r").read()
word=open("result.txt",'w')

#data sampling using combinations
for i in range(0,614):
  corpus = bully.split()
  def make_pairs(corpus):
      for i in range(len(corpus)-1):
          yield (corpus[i], corpus[i+1])
          
  pairs = make_pairs(corpus)

  word_dict = {}

  for word_1, word_2 in pairs:
      if word_1 in word_dict.keys():
          word_dict[word_1].append(word_2)
      else:
          word_dict[word_1] = [word_2]
  
  first_word = np.random.choice(corpus)

  chain = [first_word]

  n_words = 5

  for i in range(n_words):
      chain.append(np.random.choice(word_dict[chain[-1]]))

  #print(' '.join(chain))
  b.append(' '.join(chain))
with open('bully.txt','r') as inf:
    for j in inf.readlines():
        b.append(j[:-2])

for i in range(0,545):
  corpus = support.split()
  def make_pairs(corpus):
      for i in range(len(corpus)-1):
          yield (corpus[i], corpus[i+1])
          
  pairs = make_pairs(corpus)

  word_dict = {}

  for word_1, word_2 in pairs:
      if word_1 in word_dict.keys():
          word_dict[word_1].append(word_2)
      else:
          word_dict[word_1] = [word_2]
  
  first_word = np.random.choice(corpus)

  chain = [first_word]

  n_words = 5

  for i in range(n_words):
      chain.append(np.random.choice(word_dict[chain[-1]]))

  #print(' '.join(chain))
  s.append(' '.join(chain))

with open('support.txt','r') as inf:
    for j in inf.readlines():
        s.append(j[:-2])  

print("Support labelled",len(s))
print("bully labelled",len(b))
f=open("features.txt","r").readlines()
features=[]

for i in f:
    features.append(i[:-1].lower())

for i in b:
    label.append('bullying')
    comm.append(i.lower())
    word.write(i.lower()+'\n')


for i in s:
    label.append('support')
    comm.append(i.lower())
    word.write(i.lower()+'\n')

df = pd.DataFrame({'sentence':comm, 'label':label})
print(df)

##TfidfVectorizer

tfidfconverter = TfidfVectorizer(max_features=2000,vocabulary=features,ngram_range=(1, 3))  
X = tfidfconverter.fit_transform(comm).toarray()
print(X)

#Features extraction

print(len(tfidfconverter.get_feature_names()))
tfidfconverter.get_feature_names()
tfidfconverter.vocabulary_
idf=tfidfconverter.idf_

rr=dict(zip(tfidfconverter.get_feature_names(), idf))
pd.DataFrame(rr.items())

from sklearn.decomposition import TruncatedSVD
def build_lsa(x_train, dim=100):
    svd = TruncatedSVD(n_components=dim)
    
    # transformed_x_train = X.fit_transform(x_train)
    # transformed_x_test = X.transform(X_test)
    
    print('TF-IDF output shape:', x_train.shape)
    
    x_train_svd = svd.fit_transform(x_train)
    # x_test_svd = svd.transform(transformed_x_test)
    
    print('LSA output shape:', x_train_svd.shape)
    
    explained_variance = svd.explained_variance_ratio_.sum()
    
    return svd, x_train_svd

svd, X = build_lsa(X)

feature_names = np.array(tfidfconverter.get_feature_names())
sorted_by_idf = np.argsort(tfidfconverter.idf_)
print("Features with lowest idf:\n{}".format(
       feature_names[sorted_by_idf[:3]]))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.3, random_state=0)
print(X_train)
X_train.shape

from sklearn import svm


#Create a svm Classifier
text_classifier = svm.SVC(kernel='rbf')  
text_classifier.fit(X_train, y_train)

print(X_train.shape)

#save model
filename = 'model.sav'
pickle.dump(text_classifier, open(filename, 'wb'))

predictions = text_classifier.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,predictions))  
print(classification_report(y_test,predictions))  
print(accuracy_score(y_test, predictions))
l=[]

for i in input:
    l.append(i)

o=tfidfconverter.transform(l).toarray()
print(o.shape)
o=svd.transform(o)
predict=text_classifier.predict(o)

print(predict)