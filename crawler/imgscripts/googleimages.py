import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson
import json
import string

# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

allowed_extensions = ["jpg", "png", "jpeg", "jif", "jfif", "bmp", "jpeg2000"]

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

def get_extension(url):
    match = string.rfind(url, ".") 
    if match < 0:
        return "jpg"
    ext = url[match+1:]
    if ext in allowed_extensions:
        return ext
    return "jpg"


# prepare json data from courses
json_file = open('courseDetails.json')
json_data = json.load(json_file)
json_file.close()

# read the number of urls that should be downloaded for a course
url_file = open('urls_to_download.txt')
url_limit = int(url_file.read());

print url_limit

decider_file = open('decide_on_images.html', "w")
PATH = os.path.dirname(os.path.abspath(__file__))

already_have_image = os.listdir("downloaded_images")

for i in range(0, len(json_data)):

    # prepare search
    course_name_search = json_data[i]['CourseName']
    course_name_search = clean_up(course_name_search);

    print course_name_search
    decider_file.write("<h1>" + course_name_search + "</h1><br/>")

    course_name_search = course_name_search.replace(' ','%20')
    course_id = json_data[i]['CourseID']
    course_image = course_id + '.jpg'

    found = False
    for ext in allowed_extensions:
        if course_id + "." + ext in already_have_image:
            found = True
    if found:
        continue

    #print '\n'
    #print json_data[i]['Official Course Description']

    for CCOUNT in range(3):
        # request, response part
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+course_name_search+'&start=0'+'&userip=MyIP')
        request = urllib2.Request(url, None, {'Referer': 'testing'})
        try:
            response = urllib2.urlopen(request, timeout=1)
        except urllib2.URLError, e:
            continue

        # interpret json
        results = simplejson.load(response)
        if not results or not 'responseData' in results:
            continue
        data = results['responseData']
        if not data or not 'results' in data:
            continue
        dataInfo = data['results']

        count = 0

        for myUrl in dataInfo:
            #print myUrl['unescapedUrl']
            ext = get_extension(myUrl['unescapedUrl'])

            image_link = "imgs/" + course_id + "-" + str(count) + "." + ext
            myopener.retrieve(myUrl['unescapedUrl'],image_link)

            decider_file.write("<img class='img-links' src='" + PATH + "/" + image_link + "' cnt='" + str(count) + "' id='" + str(course_id) + "." + ext + "' style='height:300px;'> ")
            if count >= url_limit:
                break
            count += 1


        decider_file.write("<br/> <br/> <br/>")
        time.sleep(1)
        if count > 0:
            break

decider_file.close()