import sys
import pandas as pd
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
import pickle

class Detection:

    def main(calls, modelfile="rf_model.sav"):
        
        filename=modelfile
        train = pickle.load(open(filename, 'rb'))
        predicted_class = train.predict([calls])
        print(predicted_class[0])
        print("Successfully Predicted")
        return predicted_class[0]
        
if __name__ == "__main__":
    Detection.main('ldrloaddll ldrgetprocedureaddress ldrloaddll ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ldrgetprocedureaddress ')
    
    

