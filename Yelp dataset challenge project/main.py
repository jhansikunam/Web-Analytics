"""
start
"""

import util
import datetime
from dateutil.relativedelta import relativedelta

#Input:yelp_academic_dataset_business.json
#Get businesses and business Ids

#businesses, business_id_set = util.load_business_data('data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')

#Input:yelp_academic_dataset_review.json and filtered businessIds
#generate 'clean_reviews_csv.csv', 'clean_reviews_csv_200001.csv', 'clean_reviews_csv_400001.csv','clean_reviews_csv_600001.csv', 'clean_reviews_csv_800001.csv', 'clean_reviews_csv_1000001.csv'

#reviews = util.load_reviews_data('data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json', business_id_set)


#list of csv files generated from reviews JSON
file_name_lst = ['clean_reviews_csv.csv', 'clean_reviews_csv_200001.csv', 'clean_reviews_csv_400001.csv',
                 'clean_reviews_csv_600001.csv', 'clean_reviews_csv_800001.csv', 'clean_reviews_csv_1000001.csv']

#Generate time buckets
#Given Start Date: 2004-10-12
#Given End Date: 2016-07-19
#Given frequency: 1 year
buckets = util.generate_buckets(datetime.date(2004, 10, 12), datetime.date(2016, 7, 19), relativedelta(years=1))

#Input:businessID,time buckets and csv file list
#Generates word frequencies from reviews data for each time bucket from 2004 to 2016
bucket_counter_lst = util.gen_counter_per_bucket_business('aRkYtXfmEKYG-eTDf_qUsw', buckets, file_name_lst)

#input:buckets with word frequencies from 2004 to 2016
#generates top 10 distinctive words by comparing with consecutive buckets for given businessID:aRkYtXfmEKYG-eTDf_qUsw within the time 20014 to 2016
bucket_counter_lst_diff = util.get_bucket_counter_lst_diff(bucket_counter_lst)

#print(bucket_counter_lst)
#print(bucket_counter_lst_diff)
year=2004
# print distinctive words in each buckets
for word in bucket_counter_lst_diff:
    print(year)
    print( word)
    year=year + 1
