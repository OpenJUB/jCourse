import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson
import json

# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

def truncate(text):
    for i, c in enumerate(text):
        if (i > 20 and c == ' '):
            return text[:-(len(text)-i)]
    return text     

def clean_up(text):
    useless_keywords = [];
    with open('useless_keywords.txt') as useless_file:
        for line in useless_file:
            line = line[:-1]
            useless_keywords.append(line);
    
    for keyword in useless_keywords:
        text = text.replace(keyword, '')
    return truncate(text) 


# prepare json data from courses
json_file = open('courseDetails.json')
json_data = json.load(json_file)
json_file.close()

# read the number of urls that should be downloaded for a course
url_file = open('urls_to_download.txt')
url_limit = int(url_file.read());

print url_limit

already_have_image = os.listdir("downloaded_images")

for i in range(0, len(json_data)):

    # prepare search
    course_name_search = json_data[i]['CourseName']
    course_name_search = clean_up(course_name_search);

    print course_name_search

    course_name_search = course_name_search.replace(' ','%20')
    course_id = json_data[i]['CourseID']
    course_image = course_id + '.jpg'

    if course_image in already_have_image:
        continue

    #print '\n'
    #print json_data[i]['Official Course Description']

    if True:
        # request, response part
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+course_name_search+'&start=0'+'&userip=MyIP')
        request = urllib2.Request(url, None, {'Referer': 'testing'})
        response = urllib2.urlopen(request)

        # interpret json
        results = simplejson.load(response)
        data = results['responseData']
        dataInfo = data['results']

        count = 0

        for myUrl in dataInfo:
            #print myUrl['unescapedUrl']
            myopener.retrieve(myUrl['unescapedUrl'],course_id+'.jpg')
            count += 1
            if count >= url_limit:
                break
        time.sleep(1)