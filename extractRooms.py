import json
import re

class Room:
    def __init__(self, name):
        self.name = name
        self.events = []

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
            for activity_type in ["LEC", "SEM", "LAB"]:
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

def main():
    data = load_data('outputW25.json')
    rooms = process_data(data)
    # Example usage: Print rooms and their events
    for room in rooms:
        print(f"Room: {room.name}")
        for event in room.events:
            print(f"  Course: {event['course']}, Section: {event['section_id']}, Type: {event['type']}")
            print(f"    Time: {event['start']}-{event['end']}, Days: {event['dates']}")

if __name__ == "__main__":
    main()