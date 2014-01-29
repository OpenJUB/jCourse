from os import listdir
from os.path import isfile, join

mypath = "crawler/images/"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
filepaths = [mypath + f for f in onlyfiles]

from app.models import *
from django.core.files import File

for filepath in filepaths:
    cid = filepath.replace('.jpg','').replace(mypath, '')
    # print cid
    course = Course.objects.filter(course_id = cid)
    if len(course) == 1:
        course = course[0]
        if not course.image:
            f = open(filepath)
            myf = File(f)
            course.image = myf
            course.save()
    else:
        print "Error! There were more files with that ID!"