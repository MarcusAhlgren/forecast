import datetime
import numpy as np
import pandas as pd

def preprocess():
    """
    Prepreocess raw data.
    """
    #load data
    df = pd.read_csv("../data/raw/data.csv", sep = ";", parse_dates = ["date"])
    
    #set index column
    df = df.set_index("date")
    
    #split train and test data
    train = df.iloc[:-12]
    test = df.iloc[-12:]
    
    #save data
    train.to_pickle("../data/processed/train.pkl")
    test.to_pickle("../data/processed/test.pkl")
    
if __name__ == '__main__':
    preprocess()