import json
import datetime

class Room:
    def __init__(self, name):
        self.name = name
        self.events = []
    score = -1

def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def process_data(data):
    rooms = {}
    for course_code, course_info in data.items():
        sections = course_info.get("Sections", [])
        for section in sections:
            section_id = section.get("id")
            for activity_type in ["LEC","LAB","SEM"]:   #Rooms for Labs and Seminars are excluded, to add them just add "LAB" and "SEM"
                activity = section.get(activity_type)
                if activity:
                    location = activity.get("location", "")
                    if location:
                        parts = location.split(', ')
                        room_name = parts[-1]
                    else:
                        continue  # Skip if no location
                    start = activity.get("start")
                    end = activity.get("end")
                    dates = activity.get("date", [])
                    
                    event = {
                        "course": course_code,
                        "section_id": section_id,
                        "type": activity_type,
                        "start": start,
                        "end": end,
                        "dates": dates
                    }
                    
                    if room_name not in rooms:
                        rooms[room_name] = Room(room_name)
                    rooms[room_name].events.append(event)
    return list(rooms.values())

def get_day_abbrev(weekday):
    days = ["M", "T", "W", "Th", "F", "S", "Su"]
    return days[weekday]

#Rooms are scored based on the amount of minutes until the next event
def scoreRoom(room, weekday, givenTime):
    foundSchedule = False
    room.score = -1
    maxScore = 1440     #number of minutes in a day

    if room.name == "ROZH 102":    
        print(weekday)
        for i in room.events:
            print(i['dates'])
        print(room.score)

    for i in room.events:
        if weekday in i['dates']:
            foundSchedule = True
            #is event occuring during giventime
            if i['start'] <= givenTime <= i['end']:
                foundSchedule = True
            elif i['end'] <= givenTime: #event has already occured
                foundSchedule = True
            elif givenTime < i['start']: #event has yet to occur
                newScore = i['start'] - givenTime
                if room.score != -1:    #rooms should be scored by nearest occuring event
                    if newScore < room.score:   #if room has been scored by event occuring later
                        room.score = newScore
                elif room.score == -1:
                    room.score = newScore
                foundSchedule = True   
            if room.name == "ROZH 102":
                print(room.score)
    if foundSchedule == False:   #No events occuring during this weekday
        if room.name == "ROZH 102":
            print("did not find")
        room.score = maxScore

def scoreRoomsCurrTime(rooms):
    currtime = datetime.datetime.now()
    time = currtime.hour * 60 + currtime.minute
    weekday = get_day_abbrev(currtime.weekday())
    for i in rooms:
        scoreRoom(room=i, weekday=weekday, givenTime=time)

def scoreRoomsGivenTime(rooms, weekday, hour, minutes):
    currtime = datetime.datetime.now()

    setWeekday = weekday
    setHour = hour
    setMinutes = minutes

    if weekday == "":
        setWeekday = currtime.weekday()

    if hour == -1 or minutes == -1:
        setHour = currtime.hour
        setMinutes = currtime.minute

    print(weekday)
    print(hour)
    print(minutes)

    time = setHour * 60 + setMinutes

    for i in rooms:
        scoreRoom(room=i, weekday=setWeekday, givenTime=time)

def sortByBuilding(rooms, building):
    newRooms = []
    for room in rooms:
        roomBuilding = room.name.split()
        if len(roomBuilding) > 0 and roomBuilding[0] == building:
            newRooms.append(room)
    return newRooms

def sortRooms(rooms):
    rooms.sort(key=lambda x: x.score, reverse=True)
    
def getRooms():
    data = load_data('outputW25.json')
    rooms = process_data(data)

    scoreRoomsCurrTime(rooms)
    sortRooms(rooms)

    return rooms


# def main():

#     for room in rooms:
#         print(f"Room: {room.name}")
        #print(f"Score according to current time: {room.score}")

        # for event in room.events:
        #     print(f"  Course: {event['course']}, Section: {event['section_id']}, Type: {event['type']}")
        #     print(f"    Time: {event['start']}-{event['end']}, Days: {event['dates']}")
        #     print(index)
        #     index += 1

    # buildings = []
    # for i in rooms:
    #     building = i.name.split()
    #     if len(building) > 0 and building[0] not in buildings:
    #         buildings.append(building[0])
    # print(buildings) 

# if __name__ == "__main__":
#     main()