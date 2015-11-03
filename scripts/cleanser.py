__author__ = 'shiv'

import pandas as pd
from pprint import pprint
import csv

def listClasses():
    filepath = '../raw_data/train.csv'
    df = pd.DataFrame.from_csv(filepath, sep=',')
    series = df[df.columns[0]]
    category_set = set()
    for item in series:
        category_set.add(item)
    # pprint(category_set)
    category = 0
    category_dict = {}
    for item in category_set:
        # print item + str(category)
        category_dict[item] = category
        category += 1
    # pprint(category_dict)
    return  category_dict

def listAddress():
    filepath = '../raw_data/train.csv'
    with open(filepath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print ', '.join(row)

if __name__ == '__main__':
    # print "hello world"
    # listClasses()
    listAddress()