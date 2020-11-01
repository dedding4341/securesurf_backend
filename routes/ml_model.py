from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

import pandas as pd 
import numpy as np
import itertools
import datetime
import matplotlib.pyplot as plt

def load_data(user_email, data_points):

    if len(data_points < 100):
        return
    
    
