import json
import re
from flask import Flask, render_template, request, send_file

from coursePlanner import initData
from exportToCalendar import exportToIcal

app = Flask(__name__)

def reverseString(str):
    return str[::-1]

#ex: get CIS*2250 from CIS*2250*0102
def getCoursesName(courses):
    newCourses = []
    for i in courses:
        newCourse = reverseString(i)
        #sectionAndName: [2010,0522*SIC]
        sectionAndName = newCourse.split('*', 1)
        newCourses.append(reverseString(sectionAndName[1]))
    return newCourses

#ensure that user entered courses are present in the json file
def validateCourses(courses):
    courseList = parseCourses(courses)
    with open('outputW25NoProfNoRooms.json', 'r') as file:
        data = json.load(file)
    
    for i in courseList:
        valid = False
        for key in data:
            for j in data[key]['Sections']:
                if j['id'] == i:
                    valid = True
        if valid == False:
            return False
    return True

def parseCourses(courses):
    return re.split(r'[ ,!]+', courses)

@app.route("/", methods=["GET", "POST"])
def index():
    courses = request.form.get("courses", "")
    result = ""
    if request.method == "POST":
        if validateCourses(courses):
            courseList = parseCourses(courses)
            courseNames = getCoursesName(courseList)
            allCourseData = initData(courseNames)    
            exportToIcal(courseList, allCourseData)
            result = "successful"
            return send_file("coursePlan.ics", as_attachment=True)
        else:
            result = "Input invalid, did you forget to include the section number?"
    return render_template("index.html", result=result)


@app.route("/finder", methods=["GET", "POST"])
def finder():
    time = request.form.get("time", "")
    building = request.form.get("building", "")
    result = ""
    if request.method == "POST":
        print(time)
        print(building)
    return render_template("finder.html", result=result)
