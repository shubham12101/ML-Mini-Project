__author__ = 'shiv & shabbo!'

import pandas as pd
from pprint import pprint
import csv
from datetime import datetime
import random

CATEGORY_COL = 0
DISTRICT_COL = 3
ADDRESS_COL = 5

RAW_FILE = 0
PROCESS_FILE = 1

category_dict = {}
district_dict = {}
address_dict = {}

original_dict = {
 'ARSON': 1513,
 'ASSAULT': 76876,
 'BAD CHECKS': 406,
 'BRIBERY': 289,
 'BURGLARY': 36755,
 'DISORDERLY CONDUCT': 4320,
 'DRIVING UNDER THE INFLUENCE': 2268,
 'DRUG/NARCOTIC': 53971,
 'DRUNKENNESS': 4280,
 'EMBEZZLEMENT': 1166,
 'EXTORTION': 256,
 'FAMILY OFFENSES': 491,
 'FORGERY/COUNTERFEITING': 10609,
 'FRAUD': 16679,
 'GAMBLING': 146,
 'KIDNAPPING': 2341,
 'LARCENY/THEFT': 174900,
 'LIQUOR LAWS': 1903,
 'LOITERING': 1225,
 'MISSING PERSON': 25989,
 'NON-CRIMINAL': 92304,
 'OTHER OFFENSES': 126182,
 'PORNOGRAPHY/OBSCENE MAT': 22,
 'PROSTITUTION': 7484,
 'RECOVERED VEHICLE': 3138,
 'ROBBERY': 23000,
 'RUNAWAY': 1946,
 'SECONDARY CODES': 9985,
 'SEX OFFENSES FORCIBLE': 4388,
 'SEX OFFENSES NON FORCIBLE': 148,
 'STOLEN PROPERTY': 4540,
 'SUICIDE': 508,
 'SUSPICIOUS OCC': 31414,
 'TREA': 6,
 'TRESPASS': 7326,
 'VANDALISM': 44725,
 'VEHICLE THEFT': 53781,
 'WARRANTS': 42214,
 'WEAPON LAWS': 8555
}

def createDictionaries():
    global category_dict, address_dict, district_dict
    category_dict = getFeatureDict(CATEGORY_COL)
    address_dict = getFeatureDict(ADDRESS_COL)
    district_dict = getFeatureDict(DISTRICT_COL)
    print "Created dictionaries"

# def isNotValidData(data, sample_dict):
#     count_dict = {}
#     for key in sample_dict.keys():
#         count_dict[key] = 0
#     for row in data:
#         # print row
#         category = row[len(row)-1]
#         count_dict[category] += 1
#     for key in sample_dict.keys():
#         if count_dict[key] != sample_dict[key]:
#             return True
#     return False

def getSampleDict(min, ratio):
    sample_dict = {}
    for key in original_dict:
        if original_dict[key] < min:
            sample_dict[category_dict[key]] = int(original_dict[key] * ratio)
        else:
            sample_dict[category_dict[key]] = min
    # pprint(sample_dict)
    return sample_dict

def getDataFromFile(filename):
    data = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        csvreader.next()
        for row in csvreader:
            data.append(row)
    return data

def getClassCount():
    filename = '../raw_data/train.csv'
    class_dict = {}
    data = getDataFromFile(filename)
    for row in data:
        category = row[1]
        if category in class_dict:
            class_dict[category] += 1
        else:
            class_dict[category] = 1
    pprint(class_dict)
    avg = 0.0
    for value in class_dict.values():
        avg += value
    avg = avg / len(class_dict.values())
    print avg
    sum = 0.0
    count = 0
    for key in class_dict.keys():
        if class_dict[key] < avg:
            sum = sum + class_dict[key]
            print key + " " + str(class_dict[key])
            count += 1
    print count
    print sum / count

def getFeatureDict(column):
    filepath = '../raw_data/train.csv'
    df = pd.DataFrame.from_csv(filepath, sep=',')
    series = df[df.columns[column]]
    feature_set = set()
    for item in series:
        feature_set.add(item)
    # pprint(category_set)
    feature = 1
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

def getFeatureArrayFromString(row):
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
    return line

def getFeatureArrayFromFile(filename):
    file_data = getDataFromFile(filename)
    output_data = []
    for row in file_data:
        output_data.append(getFeatureArrayFromString(row))
    return output_data

def createSampleArray(filename, sample_dict, file_type):
    count_dict = {}
    for key in sample_dict.keys():
        count_dict[key] = 0

    file_data = getDataFromFile(filename)
    sample_data = []

    for key in category_dict:
        category_array = getCategoryArray(file_data, key)
        sample_array = getRandomSample(category_array, sample_dict[category_dict[key]])
        for row in sample_array:
            sample_data.append(getFeatureArrayFromString(row))

    # print len(sample_data)
    # pprint(sample_data)
    return sample_data

def getCategoryArray(array, category, file_type):
    output = []
    for row in array:
        if file_type ==
        cat = row[1]
        if cat == category:
            output.append(row)
    return output

def getRandomSample(array, sample_size):
    output = []
    generated_numbers = set()
    while len(output) < sample_size:
        rand = random.randint(0, len(array)-1)
        if rand in generated_numbers:
            continue
        else:
            output.append(array[rand])
    return output

def writeArrayToFile(array, outputFile):
    with open(outputFile, "wb+") as f:
        writer = csv.writer(f)
        writer.writerows(array)

def diff(list1, list2):
        return [item for item in list1 if item not in list2]

if __name__ == '__main__':
    filepath = '../raw_data/train.csv'
    createDictionaries()
    total_data = getFeatureArrayFromFile(filepath)
    sample_dict = getSampleDict(1000, 0.75)
    sample_data = createSampleArray(filepath, sample_dict)
    writeArrayToFile(sample_data, '../process_data/train_features.csv')
    test_data = diff(total_data, sample_data)
    writeArrayToFile(test_data, '../process_data/test_features.csv')
    # getTrainDict(1000, 0.75)
    # getClassCount()
    # createFeatureFile('../raw_data/train.csv', '../process_data/feature.csv')
    # getFeatureDict(3)
    # getFeatureDict(5)
    # print "hello world"
    # getClasses()
    # create()
    # listAddress()
    # print getListFromDate('2015-05-13 11:40:00')