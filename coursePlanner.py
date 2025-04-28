import itertools
import json

from CourseUtil import ScheduleItem, CourseSection, CoursePlanner

#Code from https://github.com/AlphaCloudX/Schedule-Optimizer

def initData(courses):
    course_codes = courses
    # Load the JSON file into a Python dictionary
    with open('outputW25.json', 'r') as file:
        data = json.load(file)

    allCourseData = []

    # Loop through each course code the user entered
    for course_code in course_codes:

        # Loop through every course code
        if course_code in data:
            # Find the information for the specified course code
            course_info = data[course_code]

            # Initialize the list for this course's sections
            allCourseData.append([])

            cData = course_info.get("Sections", [])

            for sec in cData:
                try:
                    lectureTime = ScheduleItem("Lecture", sec["LEC"]["start"], sec["LEC"]["end"], sec["LEC"]["date"])
                except KeyError:
                    lectureTime = None

                try:
                    semTime = ScheduleItem("Seminar", sec["SEM"]["start"], sec["SEM"]["end"], sec["SEM"]["date"])
                except KeyError:
                    semTime = None

                try:
                    labTime = ScheduleItem("Lab", sec["LAB"]["start"], sec["LAB"]["end"], sec["LAB"]["date"])
                except KeyError:
                    labTime = None

                # Create a new CourseSection with the ScheduleItems
                newSection = CourseSection(sec["id"], lectureTime, semTime, labTime)

                allCourseData[-1].append(newSection)
        else:
            pass
            print(f"Course code {course_code} not found.")
    return allCourseData