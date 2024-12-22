import itertools


class ScheduleItem:
    """
    Object to store information for a schedule item (Lecture, Seminar, or Lab)
    """

    def __init__(self, item_type, start, finish, days):
        self.item_type = item_type  # Can be 'Lecture', 'Seminar', or 'Lab'
        self.start = start
        self.finish = finish
        self.days = days

    def __str__(self):
        return f"{self.item_type}: {self.days} from {self.start} to {self.finish}"


class CourseSection:
    """
    Object to store information for a course section
    """

    def __init__(self, courseCode, lecture=None, seminar=None, lab=None):
        self.courseCode = courseCode
        self.lecture = lecture
        self.seminar = seminar
        self.lab = lab

    def __str__(self):
        result = f"Course Code: {self.courseCode}\n"
        if self.lecture:
            result += f"{self.lecture}\n"
        if self.seminar:
            result += f"{self.seminar}\n"
        if self.lab:
            result += f"{self.lab}\n"
        return result.strip()


class CoursePlanner:
    def __init__(self, courses):
        self.courses = courses
        self.combinations = self.generate_combinations()

    def generate_combinations(self):
        return list(itertools.product(*self.courses))

    def nonOverlapped(self):
        dateToIndexMap = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "Sa": 5}

        validCombinations = []

        # Locate One Of The Possible Options
        for possibleCombination in self.combinations:
            week = [[], [], [], [], [], []]  # Create an empty list for each day (M-F)

            for course in possibleCombination:
                for schedule_item in [course.lecture, course.seminar, course.lab]:
                    if schedule_item is not None:
                        for day in schedule_item.days:
                            week[dateToIndexMap[day]].append((schedule_item.start, schedule_item.finish))

            isValid = True
            for w in range(len(week)):
                # sort low to high based on the start times
                week[w] = sorted(week[w], key=lambda x: x[0])

                for c in range(1, len(week[w])):
                    if week[w][c - 1][1] >= week[w][c][0]:  # Check if finish time overlaps with next start
                        isValid = False
                        break

                if not isValid:
                    break

            if isValid:
                # print("Found Valid Combination!")
                validCombinations.append(possibleCombination)

        print(f"Possible Non Overlapping Unfiltered Combinations:\n"
              f"After: {len(validCombinations)} Before: {len(self.combinations)}")

        return validCombinations

    def print_all_schedules(self):
        combinations = self.nonOverlapped()
        for idx, combination in enumerate(combinations):
            print(f"\n\n\nSchedule for Combination {idx + 1}:")
            self.print_schedule(combination)

        print(f"\n\nAfter: {len(combinations)} Before: {len(self.combinations)}")

    def print_schedule(self, combination):
        for course in combination:
            if course.lecture:
                print(course.lecture)
            if course.seminar:
                print(course.seminar)
            if course.lab:
                print(course.lab)
