""
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
import numpy as np
import copy
from scipy.stats import chi2_contingency

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


def gen_counter_per_bucket_business(business_id, buckets, src_file_name_lst):
    business_reviews_df = pd.DataFrame()
    for name in src_file_name_lst:
        reviews_data_frame = load_csv_to_df(name)
        reviews_data_frame = reviews_data_frame[reviews_data_frame['business_id'] == business_id]
        reviews_data_frame['date']= reviews_data_frame['date'].astype('datetime64[ns]')
        reviews_data_frame = reviews_data_frame.sort(columns='date')
        reviews_data_frame['text'] = reviews_data_frame['text'].apply(text_to_word_freq_counter)
        business_reviews_df = business_reviews_df.append(reviews_data_frame)
    bucketed_dfs = bucket_df(buckets, business_reviews_df)
    bucket_counter_lst = []
    for df in bucketed_dfs:
        bucket_counter_lst.append(df[['business_id','text']].groupby(['business_id']).aggregate(np.sum)['text'].values[0])
    return bucket_counter_lst


def get_bucket_counter_lst_diff(bucket_counter_lst):
    diff = []
    for i in range(len(bucket_counter_lst)-1):
        word_and_g = []
        elements = set(bucket_counter_lst[i].elements()).union(set(bucket_counter_lst[i+1].elements()))
        total_cnt_bucket_counter_lst_i = sum(bucket_counter_lst[i].values())
        total_cnt_bucket_counter_lst_i_plus_1 = sum(bucket_counter_lst[i+1].values())
        for elm in elements:
            count_i = bucket_counter_lst[i].get(elm, 0)
            count_i_plus_1 = bucket_counter_lst[i+1].get(elm, 0)
            obs = np.array([[count_i, total_cnt_bucket_counter_lst_i - count_i],
                            [count_i_plus_1, total_cnt_bucket_counter_lst_i_plus_1 - count_i_plus_1]])
            g, p,_, _ = chi2_contingency(obs, lambda_="log-likelihood")
            word_and_g.append((elm,g))
        word_and_g.sort(key=lambda tup: tup[1], reverse=True)
        diff.append(word_and_g[:10])
    return diff

