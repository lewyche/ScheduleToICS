import pdfplumber
import re
import dateparser
from icalendar import Calendar, Event
from datetime import datetime, timedelta

# specific regex patterns for data in text
MONTHS = (
    r"january|february|march|april|may|june|july|august|september|october|november|december|"
    r"jan.|feb.|mar.|apr.|may.|jun.|jul.|aug.|sep.|oct.|nov.|dec."
    r"jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec"
)

ASSIGNMENT_KEYWORDS = (
    r"assignment|homework|project|paper|presentation|report|essay|lab\s+test"
)
TEST_KEYWORDS = (
    r"test|exam|midterm|evalutations|assessment|final"
)
QUIZ_KEYWORDS = (
    r"quiz|zybook"
)

#Excclude admistrative dates so misclassifcation doesnt arrise
ADMIN_KEYWORDS = [
    "classes",
    "lectures",
    "class",
    "first day",
    "last day",
    "thanksgiving",
    "study day",
    "drop",
    "fall break",
    "spring break",
    "winter break",
    "summer break",
    "winter session",
    "summer session",
    "winter term",
    "summer term",
    "winter semester",
    "summer semester",
]

# regex matching 
month_name_pattern = re.compile(
                    r"""#start of line
                    \b(""" + MONTHS + r""") #month names, \b ensures you dont get enmarching match
                    \s+  #Spaces, unlimted spaces 
                    (\d{1,2}) #day 
                    (?:st|nd|rd|th)? #optional suffix ending bc andrew hamilton-wright keeps writing 1st :c
                    (?:,?\s*(\d{4}))? #optional comma or space followed by year
                    \b #end of line"""
                    , re.IGNORECASE | re.VERBOSE)

assignment_pattern = re.compile(
    rf"""\b({ASSIGNMENT_KEYWORDS}|a\d{{1,2}})\b""",
    re.IGNORECASE | re.VERBOSE
)

# class to parse course outline
class courseOutlineParser:
    def __init__(self, outline: str, courseCode: str):
        """
        Stores key dates. General approach predict based on last classifer found

        self.classifier: Keeps track of last listed keyword type (assignment, test, quiz)
                         All lines are classified as such until new keyword found
                         Works relatively well for tables? may not generalize to all outlines
        """
        self.outline = outline
        self.courseCode = courseCode
        self.testDates = [] # list of test dates
        self.assignmentDates = [] # list of assignment dates
        self.quizDates = [] # list of quiz dates
        self.classifier = "" 

    def parseKeyDateGroups(self):
        """
        Parses data from course outline PDF and classifies them into groups

        Utilizes last encountered classifier to classify lines of pdf text.
        Assumption is made that lines with dates are test/quiz/assignment dates, 
        admin keywords are used to filter out non relevant lines
        """
        with pdfplumber.open(self.outline) as pdf:
            for page in pdf.pages: 
                # Iterate over each line in text converted pdf
                for line in (page.extract_text() or "").split("\n"):
                    line = line.lower()
                    if any(keyword in line for keyword in ADMIN_KEYWORDS):
                        continue

                    if assignment_pattern.search(line):
                        self.classifier = "assignment"
                    elif re.search(QUIZ_KEYWORDS, line):
                        self.classifier = "quiz"
                    elif re.search(TEST_KEYWORDS, line):
                        self.classifier = "test"

                    if month_name_pattern.search(line):
                        if self.classifier == "test":
                            self.testDates.append(line)
                        elif self.classifier == "assignment":
                            self.assignmentDates.append(line)
                        elif self.classifier == "quiz":
                            self.quizDates.append(line)
        #         # im = page.to_image(resolution=150)
        #         # im.show()

        pdf.close()
        return self

    def formatDates(self, newCalendar: Calendar):
        for test in self.testDates:
            newCalendar.add_component(self.addToCalendar(test, f"{self.courseCode} - Test: {test}"))

        for assignment in self.assignmentDates: 
            newCalendar.add_component(self.addToCalendar(assignment, f"{self.courseCode} - Assignment: {assignment}"))

        for i,quiz in enumerate(self.quizDates):
            newCalendar.add_component(self.addToCalendar(quiz, f"{self.courseCode} - Quiz: {quiz}"))
        
        return newCalendar

    def addToCalendar(self, item: str, description: str) -> Event: 
        # TO-DO: update description to not include time component

        event = Event()

        match = month_name_pattern.search(item)
        if not match:
            print("No date found in item: ", item)
            return event
        
        dateStr = match.group(0)
        date = dateparser.parse(dateStr)

        descriptionWithoutDate = re.sub(re.escape(dateStr), "", description, flags=re.IGNORECASE).strip()
        
        if date is None:
            print("Could not parse extracted date: ", dateStr)
            return event
        
        try:
            event.add('summary', descriptionWithoutDate)
            start = date.date()
            end = start + timedelta(days = 1) # make event last all day long 
            event.add('dtstart', start)
            event.add('dtend', end)

            # print("Added event: ", descriptionWithoutDate, " on ", start)
        except:
            print("invalid date parsing for item: ", item, "\n", date,start,end, "\n")


        return event