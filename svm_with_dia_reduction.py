# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class dia_red:

  def __init__(self):
      pass

  def red(self,input):
    label=[]
    comm=[]
    features=[]
    support=open("data/support.txt","r").readlines()
    bully=open("data/bully.txt","r").readlines()

    print("Support labelled",len(support))
    print("bully labelled",len(bully))
    f=open("data/features.txt","r").readlines()

    for i in f:
        features.append(i[:-1].lower())

    for i in bully:
        label.append('bullying')
        comm.append(i[:-1].lower())

    for i in support:
        label.append('support')
        comm.append(i[:-1].lower())

    df = pd.DataFrame({'sentence':comm, 'label':label})
    print(df)

    #TfidfVectorizer

    tfidfconverter = TfidfVectorizer(max_features=2000,vocabulary=features,ngram_range=(1, 3))  
    X = tfidfconverter.fit_transform(comm).toarray()

    #Features extraction

    print(len(tfidfconverter.get_feature_names()))
    tfidfconverter.get_feature_names()
    tfidfconverter.vocabulary_
    idf=tfidfconverter.idf_

    rr=dict(zip(tfidfconverter.get_feature_names(), idf))
    pd.DataFrame(rr.items())

    svd, X = self.build_lsa(X)

    feature_names = np.array(tfidfconverter.get_feature_names())
    sorted_by_idf = np.argsort(tfidfconverter.idf_)
    print("Features with lowest idf:\n{}".format(
          feature_names[sorted_by_idf[:3]]))
    
    # split into test and train
    X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.3, random_state=0,stratify=label)
    print(X_train)

    #Create a svm Classifier
    try:
      text_classifier = svm.SVC(kernel='rbf')  
      text_classifier.fit(X_train, y_train)
      print(X_train.shape)
    except Exception as e:
      print(e)
      pass


    predictions = text_classifier.predict(X_test)
    print(confusion_matrix(y_test,predictions))  
    print(classification_report(y_test,predictions))  
    print(accuracy_score(y_test, predictions))

    #predict the input
    o=tfidfconverter.transform(input).toarray()
    print(o.shape)
    o=svd.transform(o)
    print(o.shape)
    predict=text_classifier.predict(o)
    print(predict)
    return predict
  
  # diamentionality reduction
  def build_lsa(self,x_train, dim=100):
    try:
      svd = TruncatedSVD(n_components=dim)
          
      print('TF-IDF output shape:', x_train.shape)
          
      x_train_svd = svd.fit_transform(x_train)
      # x_test_svd = svd.transform(transformed_x_test)
          
      print('LSA output shape:', x_train_svd.shape)
          
      explained_variance = svd.explained_variance_ratio_.sum()
          
      return svd, x_train_svd

    except Exception as e:
      print(e)
      pass

input=['poda patti','poli sanam']
p1=dia_red()
p1.red(input)

