from .DBConnection import DBConnection
from sklearn.naive_bayes import MultinomialNB

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

import sys
from sklearn.feature_extraction.text import TfidfVectorizer


class NBClassifier():

    def start(input):
        try:
            trainset = []
            # testset=[float('0'), float('1'), float('1'),float('1'),float('0'),float('0'),float('0'),float('1')]
            # testset=
            database = DBConnection.getConnection()
            cursor = database.cursor()
            cursor.execute(
                "select * from webapp_scpattern")
            row = cursor.fetchall()
            y_train = []
            trainset.clear()
            y_train.clear()
            train=len(row)
            for r in row:

                x_train = []
                x_train.clear()
                x_train.append(str(r[2]))
                y_train.append(str(r[1]))
                
                trainset.append(x_train)
            trainset = np.array(trainset)
            
            y_train = np.array(y_train)
            print("y=", y_train)
            print("trd=", trainset)

            tfidf = TfidfVectorizer(stop_words='english',use_idf=True,smooth_idf=True)
            nb_pipeline = Pipeline([('lrgTF_IDF', tfidf), ('lrg_mn', MultinomialNB())])
            nb_pipeline.fit(trainset.flatten(), y_train.flatten())
            test = np.array(input)
            predicted_class = nb_pipeline.predict(test.flatten())
            print(predicted_class)
            return predicted_class[0]

        
        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)

if __name__ == '__main__':
    print(NBClassifier.start([' ss ss ss  ']))


