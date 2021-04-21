# -*- coding: utf-8 -*-
"""svm_classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EHBgoRIMhvqEJFWkFFPZqyrPJuBDH_Pj
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
import logging
logging.basicConfig(filename="SVM.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
logger=logging.getLogger() 
  
logger.setLevel(logging.DEBUG)
class svm_classifier:
  def __init__(self):
    self.train()

  def train(self):
    try:
      support=open("/content/support.txt","r").readlines()
      bully=open("/content/bully.txt","r").readlines()
    except:
      logger.warning("error occured during reading the files")
    label=[]
    comm=[]
    for i in bully:
      label.append('bullying')
      comm.append(i[:-1].lower())

    for i in support:
      label.append('support')
      comm.append(i[:-1].lower())
    df = pd.DataFrame({'sentence':comm, 'label':label})    
    logger.info("Loading the features")  

    try:
      f=open("/content/features.txt","r").readlines()
    except:
      logger.warning("error occured during reading features file")

    features=[]
    for i in f:
      features.append(i[:-1].lower()) 
    tfidfconverter = TfidfVectorizer(max_features=63,vocabulary=features,ngram_range=(1, 3))  
    X = tfidfconverter.fit_transform(comm).toarray()
    logger.info("vectorization using tf-idf")

    idf=tfidfconverter.idf_
    rr=dict(zip(tfidfconverter.get_feature_names(), idf))
    pd.DataFrame(rr.items())

    from sklearn.model_selection import train_test_split  
    X_train, X_test, y_train, y_test = train_test_split(X, label, test_size=0.2, random_state=0,stratify=label)
    logger.info("Spliting data into training and test")

    svm_clf = SVC(C=1,kernel='linear',gamma=1)
    svm_clf.fit(X_train, y_train)

    predictions = svm_clf.predict(X_test)
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    print(confusion_matrix(y_test,predictions))  
    print(classification_report(y_test,predictions))  
    print(accuracy_score(y_test, predictions))
    logger.info("showing the accuracy")

    input=['kidu mwone','poda thendi ']
    o=tfidfconverter.fit_transform(input).toarray()
    predict=svm_clf.predict(o)
    print(input,predict)

svm_classifier()