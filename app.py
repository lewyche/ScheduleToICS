import json
import re
from flask import Flask, render_template, request, send_file

from coursePlanner import initData
from exportToCalendar import exportToIcal

from extractRooms import getRooms, sortByBuilding, scoreRoomsGivenTime, scoreRoomsCurrTime, sortRooms

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

def fillCard(room):
    card = f"""<div class='room'>
        <h2>{room.name}</h2>
        <p>Minutes until next event: {room.score}</p>
        </div>"""
    return card


#use room data to fill html cards
def getHtmlRooms(rooms):
    htmlRooms = []
    for i in rooms:
        if i.score > 0:
            htmlRooms.append(fillCard(i))
    return htmlRooms

def setHtmlRooms():
    rooms = getRooms()
    return getHtmlRooms(rooms)


rooms = getRooms()
currTime = ""
currWeekday = ""

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
            rooms = sortByBuilding(rooms, building)
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
        

    # global currBuilding, currWeekday, currTime, rooms, htmlRooms

    # building = request.form.get("building", "")
 
    # time = request.form.get("time", "")
    # weekday = request.form.get("weekday", "")

    # reset = request.form.get("reset", "")
    # filter = request.form.get("filter", "")

    # if request.method == "POST":

    #     if weekday != "":
    #         currWeekday = weekday

    #     if time != "":
    #         currTime = time

    #     if reset == "Reset Time to Current":
    #         currTime = "reset"
    #         currWeekday = "reset"

    #     if building != "No Building" and building != "":
    #         currBuilding = building
    #     elif building == "No Building":
    #         currBuilding = "reset"
        

    #     #filter button pressed
    #     if filter == "filter":
    #         print("filtering")
    #         if currTime != "" or currWeekday != "":
    #             hour = -1
    #             minutes = -1
    #             if time != "":
    #                 splitTime = time.split(":")
    #                 hour = int(splitTime[0])
    #                 minutes = int(splitTime[1])
    #             scoreRoomsGivenTime(rooms=rooms, weekday=currWeekday, hour=hour, minutes=minutes)
    #             sortRooms(rooms)
    #             htmlRooms = getHtmlRooms(rooms)
    #         elif currTime == "reset" and currWeekday == "reset":
    #             scoreRoomsCurrTime(rooms)
    #             sortRooms(rooms)
    #             htmlRooms = getHtmlRooms(rooms)
    #             currTime = ""
    #             currWeekday = ""

    #         if currBuilding != "":
    #             rooms = getRooms()
    #             rooms = sortByBuilding(rooms=rooms, building=building)
    #             htmlRooms = getHtmlRooms(rooms)
    #         elif currBuilding == "reset":
    #             htmlRooms = setHtmlRooms()
    #             currBuilding = ""

        
        # if time != "":
        #         splitTime = time.split(":")
        #         hour = int(splitTime[0])
        #         minutes = int(splitTime[1])
        # scoreRoomsGivenTime(rooms=rooms, weekday=currWeekday, hour=hour, minutes=minutes)
        

        # #user filitered by time
        # if time != "Reset Time to Current" or (hour != "" and minutes != ""):
        #     if hour == "":
        #         hour = -1
        #     if minutes == "":
        #         minutes = -1
        #     scoreRoomsGivenTime(rooms, weekday=time, hour=hour, minutes=minutes)
        #     sortRooms(rooms)
        #     htmlRooms = getHtmlRooms(rooms)
        # elif time == "Reset Time to Current":
        #     scoreRoomsCurrTime(rooms)
        #     sortRooms(rooms)
        #     htmlRooms = getHtmlRooms(rooms)

        # #user filitered by building
        # if building != "No Building" and building != "":
        #     rooms = getRooms()
        #     rooms = sortByBuilding(rooms=rooms, building=building)
        #     htmlRooms = getHtmlRooms(rooms)
        #     currBuilding = building
        #     print("sack")
        # elif building == "No Building":
        #     htmlRooms = setHtmlRooms()
        #     currBuilding = "None"
        #     print("balls")
        # print(time)
        # print(f"{hour}:{minutes}")

    htmlRooms = getHtmlRooms(rooms)

    return render_template("finder.html", htmlRooms=htmlRooms, currTime=currTime, currWeekday=currWeekday)
