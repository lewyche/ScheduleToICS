def filterByEarliestAtSchool(schedule, startTime):
    # If the user does not want to filter by this
    if startTime == 0:
        return schedule

    dateToIndexMap = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "Sa": 5}

    validCombinations = []

    # Locate One Of The Possible Options
    for possibleCombination in schedule:
        week = [[], [], [], [], [], []]  # Create an empty list for each day (M-S)

        for course in possibleCombination:
            for schedule_item in [course.lecture, course.seminar, course.lab]:
                if schedule_item is not None:
                    for day in schedule_item.days:
                        week[dateToIndexMap[day]].append((schedule_item.start, schedule_item.finish))

        isValid = True
        for w in range(len(week)):
            # sort low to high based on the start times
            week[w] = sorted(week[w], key=lambda x: x[0])

            if week[w] and week[w][0][0] < startTime:
                isValid = False
                break

        if isValid:
            validCombinations.append(possibleCombination)

    # print(f"After: {len(validCombinations)} Before: {len(schedule)}")

    return validCombinations


def filterByLatestAtSchool(schedule, endTime):
    # If the user does not want to filter by this
    if endTime == 0:
        return schedule

    dateToIndexMap = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "Sa": 5}

    validCombinations = []

    # Locate One Of The Possible Options
    for possibleCombination in schedule:
        week = [[], [], [], [], [], []]  # Create an empty list for each day (M-S)

        for course in possibleCombination:
            for schedule_item in [course.lecture, course.seminar, course.lab]:
                if schedule_item is not None:
                    for day in schedule_item.days:
                        week[dateToIndexMap[day]].append((schedule_item.start, schedule_item.finish))

        isValid = True
        for w in range(len(week)):
            # sort low to high based on the start times
            week[w] = sorted(week[w], key=lambda x: x[0])

            if week[w] and week[w][-1][-1] > endTime:
                isValid = False
                break

        if isValid:
            validCombinations.append(possibleCombination)

    # print(f"After: {len(validCombinations)} Before: {len(schedule)}")

    return validCombinations


def filterBySpecificDayOff(schedule, daysOff):
    pass


def filterByAmountOfDaysOff(schedule, numberOfDaysOff):
    pass


def filterByTotalMinTimeBetweenClasses(schedule):
    dateToIndexMap = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "Sa": 5}

    times = []

    # Locate One Of The Possible Options
    for possibleCombination in schedule:
        week = [[], [], [], [], [], []]  # Create an empty list for each day (M-S)

        for course in possibleCombination:
            for schedule_item in [course.lecture, course.seminar, course.lab]:
                if schedule_item is not None:
                    for day in schedule_item.days:
                        week[dateToIndexMap[day]].append((schedule_item.start, schedule_item.finish))

        t = 0

        for w in range(len(week)):
            week[w] = sorted(week[w], key=lambda x: x[0])

            if week[w]:
                # Algorithm to get a start of day time

                # Get an end of date time

                # compute the length of the gaps
                for c in range(1, len(week[w])):
                    # value at times index += start of next class - end of last class
                    t += week[w][c][0] - week[w][c - 1][1]

        times.append(t)

    # Yoinked from https://stackoverflow.com/a/6423325/11521629
    # Better than using np since there is no dependency
    sortedTimeIndices = sorted(range(len(times)), key=times.__getitem__)

    # print(f"After: {len(validCombinations)} Before: {len(schedule)}")

    return schedule, sortedTimeIndices, times


def filterByAvgStartTime(schedule, sortByLatest=False):
    dateToIndexMap = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "Sa": 5}

    times = []

    # Locate One Of The Possible Options
    for possibleCombination in schedule:
        week = [[], [], [], [], [], []]  # Create an empty list for each day (M-S)

        for course in possibleCombination:
            for schedule_item in [course.lecture, course.seminar, course.lab]:
                if schedule_item is not None:
                    for day in schedule_item.days:
                        week[dateToIndexMap[day]].append((schedule_item.start, schedule_item.finish))

        t = 0
        daysOnCampus = 0

        for w in range(len(week)):
            # sort low to high based on the start times
            week[w] = sorted(week[w], key=lambda x: x[0])

            if week[w]:
                daysOnCampus += 1
                t += week[w][0][0]

        times.append(t / daysOnCampus)

    # Yoinked from https://stackoverflow.com/a/6423325/11521629
    # Better than using np since there is no dependency

    sortedTimeIndices = sorted(range(len(times)), key=times.__getitem__)

    # reverse to show the latest classes
    if sortByLatest:
        sortedTimeIndices.reverse()

    # print(f"After: {len(validCombinations)} Before: {len(schedule)}")

    return schedule, sortedTimeIndices, times
