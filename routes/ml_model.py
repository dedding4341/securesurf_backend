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
import random

rng = np.random.RandomState(42)

def word2vec(word):
    from collections import Counter
    from math import sqrt

    cw = Counter(word)
    sw = set(cw)
    lw = sqrt(sum(c*c for c in cw.values()))
    return cw, sw, lw

def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

def load_data(user_email, data_points):

    if len(data_points) < 100:
        return
    
    last_tuple = data_points.pop()
    term_list = []
    val_list = []

    for time_ms, url in data_points:
        term_list.append(url)
        val_list.append(time_ms)

    term_list_cross = random.sample(term_list, len(term_list))
    print(term_list_cross)
    x1 = []
    for term in term_list:
        running_sum = 0
        count = 0
        for word in term_list_cross:
            try:
                result = cosdis(word2vec(word), word2vec(term))
                running_sum += result
                count += 1
            except IndexError:
                pass
        x1.append(running_sum/count)
    x2 = val_list
    print(x1)
    # x_train = np.r_[x1, x1]
    # x_train = pd.DataFrame(x1, columns = ['x1', 'x2'])
    x_train = []
    for x in range(0, len(x1)):
        x_train.append([x1[x], x2[x]])
    
    print(x_train)
    x_train = np.r_[x_train, x_train]
    x_train = pd.DataFrame(x_train, columns = ['x1', 'x2'])

    x_test = 0.2 * rng.randn(last_tuple[0], 2)
    x_test = np.r_[x_test, x_test]
    x_test = pd.DataFrame(x_test, columns = ['x1', 'x2'])

    clf = IsolationForest(max_samples=100, contamination=0.1, random_state=rng)
    clf.fit(x_train)

    y_pred_train = clf.predict(x_train)
    y_pred_test = clf.predict(x_test)

    x_outliers = rng.uniform(low=0, high=1, size=(1, 2))
    x_outliers = pd.DataFrame(x_outliers, columns = ['x1', 'x2'])

    y_pred_outliers = clf.predict(x_outliers)

    print("Accuracy:", list(y_pred_test).count(1)/y_pred_test.shape[0])
    print("Accuracy:", list(y_pred_outliers).count(-1)/y_pred_outliers.shape[0])

    x_outliers = x_outliers.assign(y = y_pred_outliers)

    p1 = plt.scatter(x_train.x1, x_train.x2, c='white',
                 s=20*4, edgecolor='k')

    p2 = plt.scatter(x_outliers.loc[x_outliers.y == -1, ['x1']], 
                 x_outliers.loc[x_outliers.y == -1, ['x2']], 
                 c='red', s=20*4, edgecolor='k')
    p3 = plt.scatter(x_outliers.loc[x_outliers.y == 1, ['x1']], 
                 x_outliers.loc[x_outliers.y == 1, ['x2']], 
                 c='green', s=20*4, edgecolor='k')

    #plt.savefig('outlier_inspection.png', dpi=300)

    #plt.show()

#strings = ['lyft.com', 'reddit.com', 'google.com', 'youtube.com', 'stackoverflow.com', 'gyazo.com', 'gmail.com', 'apple.com', 'uber.com']
#sample = [(random.randint(200, 30000), random.choice(strings)) for _ in range(103)]

#load_data("email", sample)