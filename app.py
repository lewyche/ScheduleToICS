import itertools
import json
from flask import Flask, render_template, request

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

def validateCourses(courseList, allCourseData):
    for i in courseList:
        valid = False
        for j in allCourseData:
            for k in j:
                if k.courseCode == i:
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
    courseList = parseCourses(courses)
    courseNames = getCoursesName(courseList)
    allCourseData = initData(courseNames)
    if request.method == "POST":
        if validateCourses(courseList, allCourseData):
            exportToIcal(courseList, allCourseData)
            result = "successful"
        else:
            result = "try again"
    return render_template("index.html", result=result)


