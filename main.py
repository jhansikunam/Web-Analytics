"""
start
"""

import util
import datetime
from dateutil.relativedelta import relativedelta


# import numpy as np
import pandas as pd

def checkinPerBusiness(checkins):
    """
        get the count of checkins for each business
    """
    noOfCheckingPerBusi = {}
    for checkin in checkins:
        noOfCheckingPerBusi[checkin['business_id']] = noOfCheckingPerBusi.get(checkin['business_id'], 0) + 1
    return noOfCheckingPerBusi


# checkins = util.loadAndConvertJSONData(constants.FileNames['checkin'])
# print(util.sortValuesDesc(checkinPerBusiness(checkins), 20))

def averageReviewPerBusiness(reviews):
    freq = {}
    for review in reviews:
        business_id = review['business_id']
        date = review['date']
        stars = review['stars']

        if business_id in freq:
            if date in freq[business_id]:
                (T, C, F) = freq[business_id][date]
                freq[business_id][date] = (T + stars, C + 1, util.calculateAverage(T + stars, C + 1))
            else:
                freq[business_id][date] = (stars, 1, util.calculateAverage(stars, 1))
        else:
            freq[business_id] = {date: (stars, 1, util.calculateAverage(stars, 1))}
    return freq


def getFormatedData(avgReviews):
    result = []
    for k, v in avgReviews.items():
        business_id = k
        for d, a in v.items():
            date = d
            avg = a[2]
            result.append((business_id, date, avg))
    return result


# businesses, business_id_set = util.load_business_data('data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')

# reviews = util.load_reviews_data('data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json', business_id_set)

# Start Date: 2004-10-12
# End Date: 2016-07-19


file_name_lst = ['clean_reviews_csv.csv','clean_reviews_csv_200001.csv', 'clean_reviews_csv_400001.csv', 'clean_reviews_csv_600001.csv', 'clean_reviews_csv_800001.csv','clean_reviews_csv_1000001.csv']
buckets = util.generate_buckets(datetime.date(2004,10,12),datetime.date(2016,7,19), relativedelta(years = 1))
print(buckets)

business_reviews_df = pd.DataFrame()
business_id = '4bEjOyTaDG24SY5TxsaUNQ'

for name in file_name_lst:
    reviews_data_frame = util.load_csv_to_df(name)
    reviews_data_frame = reviews_data_frame[reviews_data_frame['business_id'] == business_id]
    reviews_data_frame['date']= reviews_data_frame['date'].astype('datetime64[ns]')
    reviews_data_frame = reviews_data_frame.sort(columns='date')
    reviews_data_frame['text'] = reviews_data_frame['text'].apply(util.text_to_word_freq_counter)
    business_reviews_df = business_reviews_df.append(reviews_data_frame)
bucketed_dfs = util.bucket_df(buckets, business_reviews_df)

print(business_reviews_df.iloc[[0]]['date'].values[0])


print(reviews_data_frame)
