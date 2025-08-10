import itertools
import json

from CourseUtil import ScheduleItem, CourseSection, CoursePlanner

from semesterSwitcher import getCourseData 

#Code from https://github.com/AlphaCloudX/Schedule-Optimizer


def initData(courses):
    course_codes = courses
    # Load the JSON file into a Python dictionary
    with open(getCourseData(), 'r') as file:
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
                    lectureTime = ScheduleItem("Lecture", sec["LEC"][0]["start"], sec["LEC"][0]["end"], sec["LEC"][0]["date"])
                except KeyError:
                    lectureTime = None

                try:
                    semTime = ScheduleItem("Seminar", sec["SEM"][0]["start"], sec["SEM"][0]["end"], sec["SEM"][0]["date"])
                except KeyError:
                    semTime = None

                try:
                    labTime = ScheduleItem("Lab", sec["LAB"][0]["start"], sec["LAB"][0]["end"], sec["LAB"][0]["date"])
                except KeyError:
                    labTime = None

                # Create a new CourseSection with the ScheduleItems
                newSection = CourseSection(sec["id"], lectureTime, semTime, labTime)

                allCourseData[-1].append(newSection)
        else:
            pass
            print(f"Course code {course_code} not found.")
    return allCourseData