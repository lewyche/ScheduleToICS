import itertools
import json
from flask import Flask, render_template, request, send_file

from coursePlanner import initData
from exportToCalendar import exportToIcal

app = Flask(__name__)

def reverseString(str):
    return str[::-1]

def getCoursesName(courses):
    newCourses = []
    for i in courses:
        newCourse = reverseString(i)
        sectionAndName = newCourse.split('*', 1)
        newCourses.append(reverseString(sectionAndName[1]))
    return newCourses

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
    return courses.split(" ")

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
            result = "try again"
    return render_template("index.html", result=result)


