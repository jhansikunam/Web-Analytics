"""
start
"""

import util
import datetime
from dateutil.relativedelta import relativedelta


# import numpy as np
import pandas as pd
import operator
import numpy as np


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

file_name_lst = ['clean_reviews_csv.csv', 'clean_reviews_csv_200001.csv', 'clean_reviews_csv_400001.csv',
                 'clean_reviews_csv_600001.csv', 'clean_reviews_csv_800001.csv', 'clean_reviews_csv_1000001.csv']
# Start Date: 2004-10-12
# End Date: 2016-07-19
buckets = util.generate_buckets(datetime.date(2004, 10, 12), datetime.date(2016, 7, 19), relativedelta(years=1))
bucket_counter_lst = util.gen_counter_per_bucket_business('4bEjOyTaDG24SY5TxsaUNQ', buckets, file_name_lst)
bucket_counter_lst_diff = util.get_bucket_counter_lst_diff(bucket_counter_lst)

print(bucket_counter_lst_diff)
