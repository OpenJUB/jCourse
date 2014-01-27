
import urllib
import re
import sys
import os
import lxml.html
from collections import deque
from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.insideForm = 0
        self.insideTable = 0
        self.insideCaption = 0
        self.caption = ""
        self.tableData = ""
        self.gotName = 0
        self.courseInfo = {}
    def handle_starttag(self, tag, attrs):
        if tag == "form":
            m = dict(attrs)
            if m['name'] == 'courseform' or self.insideForm > 0:
                self.insideForm += 1
        if self.insideForm and self.gotName == 0 and tag == "h1":
            self.gotName = 1
        if self.insideForm and tag == 'table':
            self.insideTable = 1
        if self.insideTable and tag == 'caption':
            self.insideCaption = 1
        if self.insideTable and tag == 'br':
            self.tableData += '<br>'
        # if self.insideTable:
        #     self.tableData += "{ "
    def handle_endtag(self, tag):
        # if self.insideTable:
        #     self.tableData += "} "
        if tag == "form" and self.insideForm > 0:
            self.insideForm -= 1
        if tag == 'table' and self.insideTable:
            self.insideTable = 0
            if self.caption != "" and self.tableData != "":
                self.courseInfo[self.caption] = self.tableData
                self.caption = ""
                self.tableData = ""
            else:
                print "Error: No caption or table contents!", self.caption
        if tag == 'caption' and self.insideCaption:
            self.insideCaption = 0
    def handle_data(self, data):
        if self.gotName == 1:
            self.courseInfo['Name'] = data
            self.gotName = 2
        if self.insideCaption:
            self.caption = data
        if self.insideTable:
            self.tableData += data
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        if self.insideTable:
            self.tableData += c
    def handle_entityref(self, name):
        if self.insideTable:
            if name in name2codepoint:
                self.tableData += chr(name2codepoint[name])
            else:
                self.tableData += "&" + name
    def getCourseInfo(self):
        return self.courseInfo

# Clean the extra things
def cleanuper(content):
    no_newlines = content.replace("\n", " ")
    no_unix_newlines = no_newlines.replace("\r", " ")
    no_tabs = no_unix_newlines.replace("\t", " ")
    no_extra_spaces = re.sub(r'  +', ' ', no_tabs)
    formatted = no_extra_spaces.replace('<br>', '\n')
    return formatted

importantFields = [ 'Instructors', 'Type', 'Org-unit', 'Course Name Abbreviation', 'Hours per week',
                    'Credits', 'Min. | Max. participants', 'Partial Grades', 'Official Course Description',
                    'Additional Information', 'This course is divided into the following sections',
                    'Further Grading Information']
linksFile = open('crawler/courses', 'r')
namesFile = open('crawler/courseNames', 'r')
outputFile = open('crawler/courseDetails', 'w')

coursesList = []

# Parse the Links
for link in linksFile:
    # Get link and print progress
    courseName = namesFile.readline()
    print courseName
    # Download the page
    page = urllib.urlopen(link)
    page = page.read()
    # Parse the page
    parser = MyHTMLParser()
    parser.feed(page)
    uglyCourseInfo = parser.getCourseInfo()
    # Delete the extra stuff and make it a dictionary
    courseInfo = dict(map(lambda x: (cleanuper(x[0]),cleanuper(x[1])), uglyCourseInfo.iteritems() ))
    if not 'Course offering details' in courseInfo:
        print "Error: No label 'Course offering details' abort scanning page"
    if not 'Name' in courseInfo:
        print "Error: No label 'Name' abort scanning page"
    # Get main details about the course
    details = courseInfo['Course offering details']
    detailsMap = {}
    # For each field found put it in the map
    for field in importantFields:
        length = len(details)
        if (field+':') in details:
            startIdx = details.find(field + ":") + len(field) + 2
            stopIdx = min( [ (details.find(f+":") if details.find(f+":") >= startIdx else length) for f in importantFields] )
            if startIdx <= stopIdx:
                if startIdx < stopIdx:
                    detailsMap[field] = unicode(details[startIdx:stopIdx], errors='ignore').strip()
            else:
                print "Error: Start after stop"
    # Parse the Catalogue information
    if 'Contained in course catalogues' in courseInfo:
        catalogue = courseInfo['Contained in course catalogues']
        startIdx = catalogue.find('> ')
        detailsMap['Catalogue'] = catalogue[startIdx+2:]
    else:
        print "Error: No label 'Contained in course catalogues'"
    detailsMap['Name'] = courseName[:-1]
    # Parse for the ID and just course name
    courseID = detailsMap['Name'][0:6]
    courseNameOnly = detailsMap['Name'][7:]
    detailsMap['CourseID'] = courseID
    detailsMap['CourseName'] = courseNameOnly
    # Add to our list
    coursesList.append(detailsMap)

linksFile.close()
namesFile.close()
outputFile.close()


# Insert results into the DB

from app.models import *

for courseDetails in coursesList:
    print courseDetails['CourseName']
    if len(Course.objects.filter(name=courseDetails['CourseName'])) > 0:
        continue
    # Setup instructors
    dbProfs = []
    instructors = courseDetails['Instructors'].split("; ")
    for instructor in instructors:
        prof = False
        profs = Professor.objects.filter(name=instructor)
        if len(profs) > 0:
            prof = profs[0]
        else:
            prof = Professor(name=unicode(instructor))
            prof.save()
        if prof:
            dbProfs.append(prof)
    # Get Course type
    ctype = False
    for CTYPE in COURSE_TYPES:
        if 'Type' in courseDetails and CTYPE[1] == courseDetails['Type']:
            ctype = CTYPE[0]
    if not ctype:
        print "Error! Didnt find course type " + courseDetails['CourseName'] + " in our models!"
        ctype = UNKNOWN
    # Get Credits number
    if 'Credits' in courseDetails:
        credits = float(courseDetails['Credits'])
    else:
        credits = 5.0
    # Create the Course class
    course = Course(course_id = courseDetails['CourseID'],
                    course_type = ctype,
                    name = courseDetails['CourseName'],
                    credits = credits,
                    catalogue = courseDetails['Catalogue'],
                    abbreviation = courseDetails['Course Name Abbreviation'])
    if 'Official Course Description' in courseDetails:
        course.description = courseDetails['Official Course Description']
    if 'Min. | Max. participants' in courseDetails and courseDetails['Min. | Max. participants'] != '- | -':
        course.participants = courseDetails['Min. | Max. participants']
    if 'Hours per week' in courseDetails:
        course.hours_per_week = courseDetails['Hours per week']
    if 'Partial Grades' in courseDetails and courseDetails['Partial Grades'] != "":
        course.grades = courseDetails['Partial Grades']
    if 'Additional Information' in courseDetails:
        course.additional_info = courseDetails['Additional Information']
    if 'This course is divided into the following sections' in courseDetails:
        course.sections_info = courseDetails['This course is divided into the following sections']
    if 'Further Grading Information' in courseDetails:
        course.grades_info = courseDetails['Further Grading Information']
    course.save()
    for dbProf in dbProfs:
        course.instructors.add(dbProf)

