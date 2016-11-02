from bs4 import BeautifulSoup
import requests
import time
import re
import urllib2
import wget
import os


def getPage(url):
    html = None
    for i in range(5):
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',})
            html = response.content
            break
        except Exception as e:
            print e
            print 'Failed attempt', i
            time.sleep(2)
    return html


def getLink(line):
    url = 'http://www.indeed.com'
    adLink = line.get('href')
    pagelink = url + str(adLink)
    return pagelink


def run(url):
    pageNum = 35  # number of pages to collect

    newpath = r'./DSNYCFTEL'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for p in range(1, pageNum + 1):  # for each page
        pageLink = url + str((p - 1) * 10)
        print pageLink
        html = getPage(pageLink)

        if not html: continue

        soup = BeautifulSoup(html)

        indeed = soup.findAll('a', {'data-tn-element': 'jobTitle'})

        for i, line in enumerate(indeed):
            getpagelink = getLink(line)
            get_job_info = getPage(getpagelink)

            with open('./DSNYCFTEL/Job{0}_{1}.html'.format(p,i), "wb") as jobFile:
                jobFile.write(get_job_info)

                # wget.download(getpagelink, './DSNYCFTEL/Job{0}.html'.format(i))
    time.sleep(2)


if __name__ == '__main__':
    url = 'http://www.indeed.com/jobs?q=data+scientist&l=NYC,+NY&rbl=New+York,+NY&jlid=45f6c4ded55c00bf&jt=fulltime&explvl=entry_level&start='
    run(url)
