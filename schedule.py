import json
import os
import classrooms
import course
import teachers
import student
import dump_to_excel

# lambda function for eliminating space at the beginning of string
remove_starting_space = lambda param: param[1:] if param[0] == " " else param


def get_classrooms_objects_list(folder_path_classrooms: str, debug: bool) -> list:
    """
    Gets the necessary data and returns a list of classrooms objects
    :param folder_path_classrooms: location of csv file
    :param debug: if you want debug information
    :return: list of classrooms objects
    """
    data_classrooms = classrooms.get_classrooms_from_csv(folder_path_classrooms, debug)

    if debug:
        print("DEBUG: list of dict of classrooms: ", data_classrooms, '\n', '_' * 20)

    # list for holding classrooms objects
    list_classrooms = []
    # create classrooms objects form the data in classrooms.csv file
    for element in data_classrooms:
        list_classrooms.append(classrooms.Classrooms(param_name=element['Name'], param_capacity=int(element['Capacity']),
                                                     param_monday=element['Monday'], param_tuesday=element['Tuesday'],
                                                     param_wednesday=element['Wednesday'], param_thursday=element['Thursday'],
                                                     param_friday=element['Friday']))

    if debug:
        print("DEBUG: list of classrooms objects: ", list_classrooms, '_' * 20)
        for element in list_classrooms:
            print("DEBUG: details classrooms objects: ", element, element.display())
            print('_' * 20)

    return list_classrooms


def get_teachers_object_list(debug: bool) -> list:
    """
    Get and parse the teacher data from the courses.json
    :param debug: if you want debug information
    :return: List of teacher objects
    """
    # read data from json file and protect against missing file
    try:
        courses_data = json.load(open(os.path.join(os.getcwd(), "courses.json"), 'r'))
    except IOError as e:
        print("ERROR %s: File does not appear to exist.", e.filename)

    if debug:
        print("DEBUG: courses.json read from get_teachers_object_list: ", courses_data, '\n', '_' * 20)

    teachers_list = []
    temp_list = []

    # get unique names of teachers
    for element in courses_data:
        tutors = element['teachers']
        # create list from enumeration
        tutors = tutors.split(',')
        # for each tutor element create a object if there isn't one
        for teacher in tutors:
            # protect against false tutors from json
            if len(teacher) > 0:
                # remove white spaces from begging of name
                teacher = remove_starting_space(teacher)
                # check if tutor exists if not add to list
                if teacher not in temp_list:
                    temp_list.append(teacher)

    if debug:
        print("DEBUG: teachers name list: ", temp_list, '\n', '_' * 20)

    # transform list of names in list of objects
    for element in temp_list:
        teachers_list.append(teachers.Teachers(element))

    if debug:
        print("DEBUG: list of teachers objects: ", teachers_list, '\n', '_' * 20)
        for element in teachers_list:
            print("DEBUG: details teachers objects: ", element, element.display())
        print('_' * 20)

    return teachers_list


def get_courses_object_list(teacher_list: list, debug: bool = False) -> list:
    """
    Get and parse the courses data from the courses.json
    :param teacher_list: list of tutors objects
    :param debug: if you want debug information
    :return: List of courses objects
    """
    if debug:
        print("DEBUG: teacher_ list got in get_courses_object_list: ", teacher_list, '\n', '_' * 20)

    # read data from json file and protect against missing file
    try:
        course_data = json.load(open(os.path.join(os.getcwd(), "courses.json"), 'r'))
    except IOError as e:
        print("ERROR %s: File does not appear to exist.", e.filename)

    if debug:
        print("DEBUG: courses.json: ", course_data, '\n', '_' * 20)

    list_courses = []
    # for each curse in the json file we create a courses objects
    for courses in course_data:
        teacher_object = None
        # get tutors for this course
        teacher = courses['teachers'].split(',')
        for teacher in teacher:
            # remove white spaces from the begging of str
            teacher = remove_starting_space(teacher)
            # find tutor object in list
            for teacher_object in teacher_list:
                if teacher_object.check_name(teacher):
                    teacher_object = teacher_object
                    # stop when find it
                    break
            # create a courses object
            list_courses.append(courses.Courses(param_name=courses['name'], param_cod=courses['code'],
                                                param_length_h=int(courses['total_h']),
                                                param_h_per_week=int(courses['week_h']),
                                                param_h_session=int(courses['session_h']),
                                                param_min_attendance=int(courses['min_part']),
                                                param_max_attendance=int(courses['max_part']),
                                                param_teacher=teacher_object))
            # add the h for the course to the tutor object associated with the course
            teacher_object.add_h_per_week(int(courses['week_h']))

    if debug:
        for element in teacher_list:
            print("DEBUG: details teachers objects: ", element, element.display())
            print('_' * 20)
        print("DEBUG: Length of list of courses objects: ", len(list_courses), '\n', '_' * 20)
        print("DEBUG: list of courses objects: ", list_courses, '\n', '_' * 20)
        for element in list_courses:
            print("DEBUG: details list_courses objects: ", element, element.display())
            print('_' * 20)

    return list_courses


def get_students_object_list(list_courses: list, debug: bool = False) -> list:
    """
    Retrivies the list of participants from json file
    :param list_courses: list of courses objects
    :param debug: if you want debug information
    :return: list of student objects sorted by the admission date
    """
    if debug:
        print("DEBUG: courses list got in get_students_object_list: ", list_courses, '\n', '_' * 20)

    # read data from json file
    try:
        students_data = json.load(open(os.path.join(os.getcwd(), "students.json"), 'r'))
    except IOError as e:
        print("ERROR %s: File does not appear to exist.", e.filename)

    if debug:
        print("DEBUG: students.json: ", students_data, '\n', '_' * 20)

    # get data from json list and transform it in a student object list
    list_students = []
    # create a student object from the data
    for element in students_data:
        list_students.append(student.Student(param_date=element['Registration date'],
                                             param_name=element['Name'], param_surname=element['Surname'],
                                             param_id=element['ID'],
                                             param_tel=element['Telephone'], param_email=element['Email'],
                                             param_wished_courses=element['Wished Courses']))
    # sort list of students by the date of admission
    list_students.sort(key=lambda x: x.date, reverse=False)

    if debug:
        print("DEBUG: Length of list of students objects: ", len(list_students), '\n', '_' * 20)
        print("DEBUG: list of students objects: ", list_students, '\n', '_' * 20)
        for element in list_students:
            print("DEBUG: details student objects: ", element, element.display())
            print('_' * 20)

    return list_students


def balance_admission(list_classrooms: list, list_students: list, list_courses: list) -> dict:
    """
    Balance the attendees of the courses for the best fit for the admission faze
    :param list_classrooms: List of classrooms objects
    :param list_students: List of students objects
    :param list_courses: List of courses objects
    :return: dictionary of courses code and best fit for attendee
    """
    # dict_courses['cod'] = [nr_attendees, nr_courses, min_course_value, max_courses_value]
    dict_courses = dict()
    # get max capacity of a course from rooms
    max_capacity = 0
    for room in list_classrooms:
        if room.capacity > max_capacity:
            max_capacity = room.capacity
    # find all possible attendees per course
    for attendee in list_students:
        for courses in attendee.get_courses():
            if courses not in dict_courses.keys():
                dict_courses[courses] = [0, 0, 0, 0]
            else:
                dict_courses[courses][0] += 1
    # find the number of courses with same code
    for courses in list_courses:
        if courses.get_code() in dict_courses.keys():
            (dict_courses[courses.get_code()])[1] += 1
            (dict_courses[courses.get_code()])[2] = courses.min_attendance
            (dict_courses[courses.get_code()])[3] = courses.max_attendance
    # change dict to hold the best value for each course
    for key in dict_courses.keys():
        # find out how many courses are needed to distribute all attends at min
        min_att = dict_courses[key][0] / dict_courses[key][2]
        # change the number of courses to average to
        nr_courses = min(min_att, dict_courses[key][1])
        # calculate the best value of attendees per course
        tmp = int(dict_courses[key][0] / nr_courses + 0.5)
        if tmp > dict_courses[key][2]:
            if dict_courses[key][3] > max_capacity:
                dict_courses[key] = max_capacity
            else:
                dict_courses[key] = dict_courses[key][3]
        else:
            dict_courses[key] = max(tmp, dict_courses[key][2])

    return dict_courses


def generate_schedule(folder_path_classrooms: str, debug: bool = False) -> bool:
    """
    Function for generation schedule for each room
    :param folder_path_classrooms: location of classrooms csv file
    :param debug: if you want debug information
    :return: Trie of the schedule was OK generated
    """
    # list for holding classrooms objects
    list_classrooms = get_classrooms_objects_list(folder_path_classrooms, debug)
    # list for holding teachers objects
    list_teacher = get_teachers_object_list(debug)
    # list for holding courses objects
    list_courses = get_courses_object_list(list_teacher, debug)
    # list for holding students objects
    list_students = get_students_object_list(list_courses, debug)

    # get number of attendees for each course so we can calculate the best attendees for a course
    dict_courses = balance_admission(list_classrooms, list_students, list_courses)
    # change max attendee for each course with best fit value
    for all_course in list_courses:
        if all_course.get_code() in dict_courses.keys():
            all_course.set_max_attendance(dict_courses[all_course.get_code()])

    # sort the courses according to max attendance to see which course is most popular
    list_courses.sort(key=lambda x: x.max_attendance, reverse=True)
    # take out courses that can cause tutors to have to much hours.
    for teacher in list_teacher:
        if teacher.check_weekly_hours() is not True:
            # the courses by the best fit so the last was is the one with less desired attendee
            # we start from the last one and move to the first
            for index in range(len(list_courses) - 1, 0, -1):
                if list_courses[index].get_teacherr() == teacher:
                    list_courses[index].set_invalid()
                if teacher.check_weekly_hours() is True:
                    # stop when the tutor has the appropriate max hours.
                    break

    # see what courses can be activated for each student object
    for attendee in list_students:
        # go throw each course option of student object
        for option in attendee.get_courses():
            # find first course with proper code
            for all_course in list_courses:
                if all_course.check_course_size() and all_course.check_code(option) and all_course.valid:
                    all_course.add_student(attendee)
                    attendee.add_course(option, all_course.get_h_week())
                    # stop because one attendee can't by in 2 instances of the same course
                    break

    # clear inactive courses after adding all the student objects to a course object
    for all_course in list_courses:
        if all_course.check_course_validity() is False:
            all_course.set_invalid()

    if debug:
        for element in list_courses:
            if element.valid:
                print("DEBUG: Active course: ", element, element.display())
                print("_" * 20)

    # sort the courses according to actual attendee
    list_courses.sort(key=lambda x: x.nr_attendance_actual, reverse=True)
    # sort the rooms according to max capacity
    list_classrooms.sort(key=lambda x: x.capacity, reverse=True)

    # counter for holding courses that been added
    counter = 0
    # add all activated courses in a week
    for all_course in list_courses:
        if all_course.valid:
            # calculate the number of sessions per week
            sessions_to_add = int(all_course.h_per_week / all_course.h_session)
            # create a unique code in the schedule for each course
            cod_to_add = all_course.cod + "_" + str(counter)
            # parse each classrooms object to see where can we add the course
            for room in list_classrooms:
                # try to keep sessions in same room
                while sessions_to_add:
                    # check if the room has how to accommodate the remaining sessions
                    if room.is_free_slots(all_course.h_session) and (sessions_to_add <= room.free_days_per_week()):
                        if room.add_course_to_classroom(cod_to_add, all_course.h_session):
                            sessions_to_add -= 1
                            all_course.set_max_attendance(room.capacity)
                        else:
                            # all day's are invalid for this room: no time slot or course already in that day
                            break
                    else:
                        # room has no capacity
                        break
                if sessions_to_add == 0:
                    counter += 1
                    # stop loop because we finished to add sessions
                    break

    # check that all attendees respect the maxi h quota
    for attendee in list_students:
        if attendee.check_h_per_week() is not True:
            # get courses desired by student object and reverse the list so we start with the least desired
            wished_courses = list(attendee.get_courses())
            wished_courses.reverse()
            # check all active courses for the one the attendee is in
            for wished_course in wished_courses:
                if attendee.check_course_active(wished_courses):
                    for all_course in list_courses:
                        if all_course.get_code() == wished_course and attendee in all_course.list_attendance:
                            all_course.remove_student(attendee)
                            attendee.clear_course(wished_course, all_course.h_per_week)
                            # can't attend multiple instances of same course
                            break
                if attendee.check_h_per_week() is True:
                    # stop iteration because the attendee respects the h rule
                    break

    # Adjust courses to size of room allocated
    for all_course in list_courses:
        balance_list = all_course.balance_attendes_course()
        # try to relocate students to same course other teacher
        for tmp_course in list_courses:
            if all_course.get_code() == tmp_course.get_code() and tmp_course.check_course_size():
                while len(balance_list) > 0 and tmp_course.check_course_size():
                    tmp_course.add_student(balance_list.pop(0))
        # clear the curses from the students objects that couldn't be relocated
        for element in balance_list:
            element.clear_course(all_course.cod, all_course.h_per_week)

    if debug:
        for element in list_classrooms:
            element.display()
            print("_" * 20)

    # get the number of weeks for the courses
    max_weeks = 0
    for all_course in list_courses:
        if all_course.valid:
            weeks = all_course.get_weeks()
            if max_weeks < weeks:
                max_weeks = weeks

    if debug:
        print("DEBUG: Weeks for semester: ", max_weeks, "\n", "_" * 20)

    generate_results = True
    # print and generate xls for each room
    for room in list_classrooms:
        room.display_schedule()
        if dump_to_excel.dump_to_excel_room(room, max_weeks):
            print("Excel writen OK for room:", room.name)
        else:
            generate_results = False

    return generate_results



if __name__ == "__main__":
    pass