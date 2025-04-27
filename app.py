import json
import re
from flask import Flask, render_template, request, send_file

from coursePlanner import initData
from exportToCalendar import exportToIcal

from extractRooms import getRooms, filterByBuilding, scoreRoomsGivenTime, scoreRoomsCurrTime, sortRooms

app = Flask(__name__)

#==Global variables for class finder==

rooms = getRooms()
currTime = ""
currWeekday = ""

#Helper functions for Schedule Importer Page

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

def fillCard(room):
    card = f"""<div class='room'>
        <h2>{room.name}</h2>
        <p>Minutes until next event: {room.score}</p>
        </div>"""
    return card

#Helper Functions for classroom finder page

#use room data to fill html cards
def getHtmlRooms(rooms):
    htmlRooms = []
    for i in rooms:
        if i.score > 0:
            htmlRooms.append(fillCard(i))
    return htmlRooms

def sortAndScoreRooms():
    global rooms, currTime, currWeekday
    hour = -1
    minutes = -1
    if currTime != "":
        splitTime = currTime.split(":")
        hour = int(splitTime[0])
        minutes = int(splitTime[1])
    scoreRoomsGivenTime(rooms=rooms, weekday=currWeekday, hour=hour, minutes=minutes)
    sortRooms(rooms)

@app.route("/finder", methods=["GET", "POST"])
def finder():
    global rooms, currTime, currWeekday

    building = request.form.get("building", "")
    time = request.form.get("time", "")
    weekday = request.form.get("weekday", "")

    reset = request.form.get("reset", "")

    if request.method == "POST":

        if building != "No Building" and building != "":
            rooms = getRooms()
            rooms = filterByBuilding(rooms, building)
            sortAndScoreRooms()
        elif building == "No Building":
            rooms = getRooms()
            sortAndScoreRooms()        
            
        if time != "":
            currTime = time
            sortAndScoreRooms()

        if weekday != "":
            currWeekday = weekday
            sortAndScoreRooms()

        if reset == "Reset Time to Current":
            scoreRoomsCurrTime(rooms)
            sortRooms(rooms)
            currTime = ""
            currWeekday = ""
        
    htmlRooms = getHtmlRooms(rooms)

    return render_template("finder.html", htmlRooms=htmlRooms, currTime=currTime, currWeekday=currWeekday)


