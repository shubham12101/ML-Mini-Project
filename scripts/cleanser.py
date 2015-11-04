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
original_dict = {}
category_list = [
'ARSON',
'ASSAULT',
'BAD CHECKS',
'BRIBERY',
'BURGLARY',
'DISORDERLY CONDUCT',
'DRIVING UNDER THE INFLUENCE',
'DRUG/NARCOTIC',
'DRUNKENNESS',
'EMBEZZLEMENT',
'EXTORTION',
'FAMILY OFFENSES',
'FORGERY/COUNTERFEITING',
'FRAUD',
'GAMBLING',
'KIDNAPPING',
'LARCENY/THEFT',
'LIQUOR LAWS',
'LOITERING',
'MISSING PERSON',
'NON-CRIMINAL',
'OTHER OFFENSES',
'PORNOGRAPHY/OBSCENE MAT',
'PROSTITUTION',
'RECOVERED VEHICLE',
'ROBBERY',
'RUNAWAY',
'SECONDARY CODES',
'SEX OFFENSES FORCIBLE',
'SEX OFFENSES NON FORCIBLE',
'STOLEN PROPERTY',
'SUICIDE',
'SUSPICIOUS OCC',
'TREA',
'TRESPASS',
'VANDALISM',
'VEHICLE THEFT',
'WARRANTS',
'WEAPON LAWS'
]


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

def getSampleDict(min, ratio, file_type):
    sample_dict = {}
    # print "The sample dictionary is : "
    if file_type == RAW_FILE:
        for key in original_dict:
            if original_dict[key] < min:
                sample_dict[category_dict[key]] = int(original_dict[key] * ratio)
            else:
                sample_dict[category_dict[key]] = min
        # pprint(sample_dict)
        return sample_dict
    else:
        for item in category_list:
            if original_dict[str(category_dict[item])] < min:
                sample_dict[str(category_dict[item])] = int(original_dict[str(category_dict[item])] * ratio)
            else:
                sample_dict[str(category_dict[item])] = min
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

def getClassCount(filename, file_type):
    global original_dict
    data = getDataFromFile(filename)
    for row in data:
        if file_type == RAW_FILE:
            category = row[1]
        else:
            category = row[len(row)-1]
        if category in original_dict:
            original_dict[category] += 1
        else:
            original_dict[category] = 1
    # return class_dict
    # print "The original dictionary is : "
    # pprint(original_dict)
    # avg = 0.0
    # for value in class_dict.values():
    #     avg += value
    # avg = avg / len(class_dict.values())
    # print avg
    # sum = 0.0
    # count = 0
    # for key in class_dict.keys():
    #     if class_dict[key] < avg:
    #         sum = sum + class_dict[key]
    #         print key + " " + str(class_dict[key])
    #         count += 1
    # print count
    # print sum / count

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
    file_data = getDataFromFile(filename)
    sample_data = []

    # pprint(file_data)

    for key in category_dict:
        if file_type == RAW_FILE:
            category_array = getCategoryArray(file_data, key, file_type)
            sample_array = getRandomSample(category_array, sample_dict[category_dict[key]])
            for row in sample_array:
                sample_data.append(getFeatureArrayFromString(row))
        else:
            category_array = getCategoryArray(file_data, category_dict[key], file_type)
            # pprint(category_array)
            sample_array = getRandomSample(category_array, sample_dict[str(category_dict[key])])
            for row in sample_array:
                sample_data.append(row)
    # print len(sample_data)
    # pprint(sample_data)
    return sample_data

def getCategoryArray(array, category, file_type):
    output = []
    print category
    # print file_type
    for row in array:
        if file_type == RAW_FILE:
            cat = row[1]
            if cat == category:
                output.append(row)
        else:
            cat = row[len(row)-1]
            if cat == str(category):
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
    filepath = '../process_data/test_features.csv'
    createDictionaries()
    getClassCount(filepath, PROCESS_FILE)
    # total_data = getFeatureArrayFromFile(filepath)
    sample_dict = getSampleDict(2000, 1, PROCESS_FILE)
    # pprint(original_dict)
    # pprint(sample_dict)
    # pprint(sample_dict)
    sample_data = createSampleArray(filepath, sample_dict, PROCESS_FILE)
    # pprint(sample_data)
    writeArrayToFile(sample_data, '../process_data/test_final_features.csv')
    # test_data = diff(total_data, sample_data)
    # writeArrayToFile(test_data, '../process_data/test_features.csv')
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