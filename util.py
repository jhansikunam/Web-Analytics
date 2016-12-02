"""
 A simple python script that contains all the helper/util functions. This functions can be used by other scripts.
"""
import json
import os
import csv
import re
from collections import Counter
from operator import itemgetter
import pandas as pd
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english'))


def load_reviews_data(reviews_file_name, business_id_set):
    reviews_list = []
    file = open(reviews_file_name)
    first = True
    counter = 0
    start_index = 0
    end_index = 200000
    file_name = 'clean_reviews_csv'
    csvFile = open(file_name+'.csv', 'w')

    for jsonText in file:
            jsontopy = json.loads(jsonText)
            if jsontopy['business_id']  in business_id_set:
                jsontopy['votes_funny'] = jsontopy['votes']['funny']
                jsontopy['votes_cool'] = jsontopy['votes']['cool']
                jsontopy['votes_useful'] = jsontopy['votes']['useful']
                jsontopy.pop('votes', None)
                if first:
                    writer = csv.DictWriter(csvFile, fieldnames=jsontopy.keys())
                    writer.writeheader()
                    first = False
                counter += 1
                if counter % 100000 == 0:
                    print (counter)
                writer.writerow(jsontopy)

            if end_index == counter:
                start_index = end_index + 1
                end_index += 200000
                csvFile.close()
                csvFile = open(file_name+'_'+str(start_index)+'.csv', 'w')
                first = True
    csvFile.close()
    file.close()
    return reviews_list


def load_business_data(business_file_name):

    business_list = []
    business_id_set = set([])
    file = open(business_file_name)
    csvFile = open(business_file_name.split('.')[0]+'_csv.csv', 'w')
    counter = 0
    first = True

    for jsonText in file:

        jsonToPy = json.loads(jsonText)
        if 'Restaurants' in jsonToPy['categories'] and jsonToPy['review_count'] >= 100:
            business_list.append(jsonToPy)
            if first:
                writer = csv.DictWriter(csvFile, fieldnames=jsonToPy.keys())
                writer.writeheader()
                first = False
                counter += 1
            writer.writerow(jsonToPy)
            business_id_set.add(jsonToPy['business_id'])

    csvFile.close()
    file.close()
    return business_list, business_id_set


def text_to_word_freq_counter(txt):
    txt = txt.lower()
    words = re.sub('[^a-z]',' ', txt).split()
    words = filter(lambda word: word not in STOP_WORDS, words)
    return Counter(words)


def convert_dict_to_dataframe(row_dict_lst):
    df = pd.DataFrame.from_dict(row_dict_lst)
    del row_dict_lst
    return df


def generate_buckets(start_date, end_date, frequency):
    buckets = []
    while start_date < end_date:
        buckets.append((start_date, start_date + frequency))
        start_date += frequency
    return buckets


def bucket_df(buckets, df):
    bucketed_dfs = []
    for bucket in buckets:
        mask = (df['date'] >= bucket[0])&(df['date']<=bucket[1])
        bucketed_dfs.append(df[mask])
    return bucketed_dfs


def load_csv_to_df(path):
    return pd.read_csv(path)





def convertPyToJson(pyData):
    """
     This function takes a python object (List, Dict, Set, Boolean, String, Integer) and returns an equivalent json object
    """
    return json.dumps(pyData)


def getAbsFileName(fname):
    fileAbsPath = os.path.abspath(fname)
    return fileAbsPath


def write_dict_to_CSV(csv_file, dict_data):
    try:
        with open(csv_file, 'w') as csvFile:
            writer = csv.DictWriter(csvFile)
            for data in dict_data:
                writer.writerow(data)
    except IOError as err:
        print (err)
    return


def sortValuesDesc(dataDict, k):
    """
        sort the dictionary by value, in descending order and return the k top records
    """
    sortedByValue = sorted(dataDict.items(), key=itemgetter(1), reverse=True)
    return sortedByValue[:k]  # return the top k terms and their frequencies


def calculateAverage(T, C):
    return T / C


def writeDataToJSON(fname, headers, data):
    f = csv.writer(open(fname + ".csv", "w"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(headers)

    # Write the data to csv
    for rec in data:
        f.writerow(rec)

    print(fname + ".csv", "successfully created")
