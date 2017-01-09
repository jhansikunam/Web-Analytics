Instructions

Run main.py to get the final output

The below files are created after cleaning 
'clean_reviews_csv.csv',
'clean_reviews_csv_200001.csv', 
‘clean_reviews_csv_400001.csv',
'clean_reviews_csv_600001.csv', 
'clean_reviews_csv_800001.csv', 
'clean_reviews_csv_1000001.cs

businesses, business_id_s and reviews are commented out as we already cleaned the data.
If the cleaning is required again please run businesses, business_id_s and reviews by removing the comments and by giving yelp_academic_dataset_business.json and yelp_academic_dataset_review.json respectively.

We have executed the code for one business ID:aRkYtXfmEKYG-eTDf_qUsw

If you want to check for any other business ID please give the business id in below line in main.py
bucket_counter_lst = util.gen_counter_per_bucket_business('aRkYtXfmEKYG-eTDf_qUsw', buckets, file_name_lst)
