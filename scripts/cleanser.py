__author__ = 'shiv & shabbo'

import pandas as pd
from pprint import pprint
import csv
from datetime import datetime

CATEGORY_COL = 0
DISTRICT_COL = 3
ADDRESS_COL = 5

def getFeatureDict(column):
    filepath = '../raw_data/train.csv'
    df = pd.DataFrame.from_csv(filepath, sep=',')
    series = df[df.columns[column]]
    feature_set = set()
    for item in series:
        feature_set.add(item)
    # pprint(category_set)
    feature = 0
    feature_dict = {}
    for item in feature_set:
        # print item + str(category)
        feature_dict[item] = feature
        feature += 1
    # pprint(feature_dict)
    # print len(feature_dict)
    return feature_dict

def getListFromDate(str):
    dObject = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    dateList = []
    dateList.append(dObject.year)
    dateList.append(dObject.month)
    dateList.append(dObject.hour)
    return dateList

def getFeature(filename):
    category_dict = getFeatureDict(CATEGORY_COL)
    district_dict = getFeatureDict(DISTRICT_COL)
    address_dict = getFeatureDict(ADDRESS_COL)
    data = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        csvreader.next()
        for row in csvreader:
            line = []
            # print row[0]
            category = category_dict[row[1]]
            dateList = getListFromDate(row[0])
            district = district_dict[row[4]]
            address = address_dict[row[6]]
            for item in dateList:
                line.append(item)
            line.append(district)
            line.append(address)
            line.append(category)
            # pprint(line)
            data.append(line)
    return data

def createFeatureFile(inputFile, featureFile):
    data = getFeature(inputFile)
    with open(featureFile, "wb+") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def divideData(originalFile, trainFile, testFile):
    csvfile =  open(originalFile, 'rb')
    csvfile1 =  open(trainFile, 'wb+')
    csvfile2 =  open(testFile, 'wb+')
    csvreader = csv.reader(csvfile, delimiter=',')
    csvwriter1 = csv.writer(csvfile1)
    csvwriter2 = csv.writer(csvfile2)
    i = 1
    for row in csvreader:
        if i % 3 == 0:
            csvwriter2.writerow(row)
        else:
            csvwriter1.writerow(row)
        i = i + 1
    csvfile.close()
    csvfile1.close()
    csvfile2.close()

if __name__ == '__main__':
    divideData('../process_data/feature.csv','../process_data/feature_train.csv','../process_data/feature_test.csv')
    # createFeatureFile('../raw_data/train.csv', '../process_data/feature.csv')
    # getFeatureDict(3)
    # getFeatureDict(5)
    # print "hello world"
    # getClasses()
    # create()
    # listAddress()
    # print getListFromDate('2015-05-13 11:40:00')