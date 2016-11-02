from bs4 import BeautifulSoup
import re
import urllib2
from operator import itemgetter
import time
import sys
import requests
from collections import Counter
import string


def getPage(url):
    html = None
    for i in range(5):
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',})
            html = response.content
            break
        except Exception as e:
            print 'Failed attempt', i
            time.sleep(2)
    return html


def getCritic(review):
    critic = 'NA'
    critic_chunk = review.find('a', {'href': re.compile('/critic/')})
    if critic_chunk:
        critic = critic_chunk.text.encode('ascii', 'ignore')
    return critic


def getTextLen(review):
    text = 'NA'
    textChunk = review.find('div', {'class': 'the_review'})
    valid=string.ascii_letters
    lst=[]
    if textChunk:
        textChunk = textChunk.text.encode('ascii', 'ignore')
        count=Counter(textChunk)
        for letter in valid:
            lst.append(count[letter])
    text = sum(lst)
    return str(text)


def getRating(review):

    rating = 'NA'
    get_content=[]
    rating_chunk = review.find('div', {'class': re.compile('review_icon')})
    if rating_chunk:
        get_content=rating_chunk.get('class')
        rating=get_content[3]

    return rating


def getSource(review):
    source='NA'
    source_chunk = review.find('em',{'class': 'subtle'})
    if source_chunk:
        source = source_chunk.text.encode('ascii', 'ignore')
    return source

def getDate(review):
    date='NA'
    date_chunk = review.find('div', {'class': 'review_date subtle small'})
    if date_chunk:
        date=date_chunk.text.encode('ascii', 'ignore')
    return date


def run(url):

    fw = open('reviews.txt', 'w')

    html = getPage(url)
    if not html:
        time.sleep(2)

    soup = BeautifulSoup(html)  # parsehtml
    reviews = soup.findAll('div', {'class': re.compile('review_table_row')})
    for review in reviews:
        critic = getCritic(review)
        rating=getRating(review)
        source=getSource(review)
        date=getDate(review)
        text = getTextLen(review)


        fw.write(critic + '\t' + rating + '\t' + source + '\t' + date + '\t' + text + '\n')

    time.sleep(2)
    fw.close()


if __name__ == '__main__':
    url = 'https://www.rottentomatoes.com/m/space_jam/reviews/'
    run(url)
