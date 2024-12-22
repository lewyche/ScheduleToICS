from icalendar import Calendar, Event, vDatetime
from datetime import datetime
import zoneinfo

def exportToIcal(courses, allCourseData):
    newCal = Calendar()
    for c in courses:
        for i in allCourseData:
            for j in i:
                if j.courseCode == c.courseCode:
                    addSectionItems(j, newCal)
    #to_ical() returns bytes, so writing in binary is necessary 
    newIcs = open("coursePlan.ics", 'wb')
    newIcs.write(newCal.to_ical())
    print("Calendar exported.")
    newIcs.close()

#add section items to calendar
def addSectionItems(item, cal):
    if item.lecture != None:
        newEvent = addScheduleItem(item.courseCode, item.lecture, cal)
    if item.seminar != None:
        newEvent = addScheduleItem(item.courseCode, item.seminar, cal)
    if item.lab != None:
        newEvent = addScheduleItem(item.courseCode, item.lab, cal)

#add schedule items to calendar
def addScheduleItem(courseCode, item, cal):
    for i in item.days:            
        newEvent = Event()
        newEvent.add('summary', courseCode + ' ' + item.item_type)
        #start of the event
        newEvent.add('dtstart', getScheduleItemDateTime(item, item.start, i))
        #end of the event
        newEvent.add('dtend', getScheduleItemDateTime(item, item.finish, i))
        #reoccur every week until the last day of class: April 4, 2025
        lastDay = datetime(2025,4,4,0,0,0,0,tzinfo=zoneinfo.ZoneInfo("America/New_York"))
        newEvent.add('rrule', {'freq': 'weekly', 'until': lastDay})
        #add event to calendar
        cal.add_component(newEvent)

#get first time a schedule item occurs on "day"
def getScheduleItemDateTime(item, time, day):
    year = 2025
    month = 1
    hour = int(time / 60)
    minutes = time - hour * 60
    return datetime(year, month, getFirstDay(day), hour, minutes, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))

#the day a course starts
def getFirstDay(day):
    week = ['M','T','W','Th','F', 'Sa']
    #dates of weekdays in the first week
    dates = [6,7,8,9,10,11]
    i = week.index(day)
    if(i != -1):
        return dates[i]
    else:
        print("getFirstDay(): invaild weekday")
        return 0
