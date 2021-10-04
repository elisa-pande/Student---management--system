from teachers import Teachers as Teachers
from student import Student as Student


class Courses:
    def __init__(self, param_name: str, param_code: str, param_length_h: int, param_h_per_week: int,
                 param_h_session: int, param_min_attendance: int, param_max_attendance: int,
                 param_teacher: Teachers) -> None:
        """
        Constructor of class
        :param param_name: name of the course
        :param param_code: Abbreviation of the course
        :param param_length_h: total course duration in h
        :param param_h_per_week: course h in a week
        :param param_h_session: course h in a session
        :param param_min_attendance: min attendees for this course
        :param param_max_attendance: max attendees for this course
        :param param_teacher: tutor of the course. This is a tutor object
        """
        # min number of attendance
        self.min_students = 10
        # name of the course
        self.name = param_name
        # the abbreviation of the course
        self.code = param_code
        # the number of hours per semester
        self.length_h = param_length_h
        # number of hours per week
        self.h_per_week = param_h_per_week
        # number of hours per session
        self.h_session = param_h_session
        if param_min_attendance < self.min_students:
            # minimum attendance
            self.min_attendance = self.min_students
        else:
            self.min_attendance = param_min_attendance
        # max attendance
        self.max_attendance = param_max_attendance
        # actual attendance
        self.nr_attendance_actual = 0
        # TODO make check for teacher type
        self.teacher = param_teacher
        # list of attendance
        self.list_attendance = []
        # is course active or not
        self.valid = True

    def get_h_week(self) -> int:
        """
        :return: the number of h in a week of the course
        """
        return int(self.h_per_week)

    def get_code(self) -> str:
        """
        :return: the code of the course
        """
        return self.code

    def check_code(self, code: str) -> bool:
        """
        :param code: string to be verified against course code
        :return: True if there are equal
        """
        return code == self.code

    def check_course_size(self) -> bool:
        """
        :return: True if the course size is in limits
        """
        return self.nr_attendance_actual < self.max_attendance

    def balance_attendees_course(self) -> list:
        """
        This function is used to get attendees that are over the max
        capacity after modifying the max capacity
        :return: list of attendees that are over the max number of attendees
        """
        list_to_return = []
        if not self.check_course_size():
            list_to_return = self.list_attendance[self.max_attendance - 1:]
            self.list_attendance = self.list_attendance[:self.max_attendance]
            self.nr_attendance_actual = self.max_attendance
        return list_to_return

    def check_course_validity(self) -> bool:
        """
        :return: True if the course is valid from the point of number of attendees
        """
        return self.min_attendance <= self.nr_attendance_actual <= self.max_attendance

    def add_student(self, attendee: Student) -> None:
        """
        :param attendee: student object to be added in the list of attendees
        :return: None
        """
        self.list_attendance.append(attendee)
        self.nr_attendance_actual += 1

    def remove_student(self, attendee: Student) -> None:
        """
        :param attendee: student object to be removed from the list of attendees
        :return: None
        """
        self.list_attendance.remove(attendee)
        self.nr_attendance_actual -= 1

    def set_max_attendance(self, value: int) -> None:
        """
        :param value: The value to modify the max attendees of the course
        :return: None
        """
        self.max_attendance = value

    def set_invalid(self) -> None:
        """
        Sets the course invalid.
        Removes all the attendees from the list.
        :return: None
        """
        # reduce the h from the tutors week
        self.teacher.reduce_h_per_week(self.h_per_week)
        # clear attendees from course
        for attendee in self.list_attendance:
            attendee.clear_course(self.code, self.h_per_week)

        self.list_attendance.clear()
        # set course to invalid
        self.valid = False

    def get_weeks(self) -> int:
        """
        :return: Number of week for the course
        """
        return int(self.length_h / self.h_per_week + 0.5)

    def get_tutor(self) -> Teachers:
        """
        :return: Tutor object for the course
        """
        return self.teacher

    def display(self) -> None:
        """
        Prints the information for the course
        :return:
        """
        print("Name:", self.name)
        print("Code:", self.code)
        print("Total hours:", self.length_h)
        print("Hours per week:", self.h_per_week)
        print("Hours per session:", self.h_session)
        print("Min attendances:", self.min_attendance)
        print("Max attendances:", self.max_attendance)
        print("Current attendees:", self.nr_attendance_actual)
        print("Teachers:", self.teacher)
        print("MIN_STUDENTS:", self.min_students)
        print("list_attendance:", self.list_attendance)
        print("valid:", self.valid)

    # TODO add necessary methods


if __name__ == "__main__":
    # test class
    t1 = Teachers("Ion Vasile")

    c1 = Courses(param_name="Programming Basic 1", param_code="PB1", param_length_h=50, param_h_per_week=4,
                 param_h_session=2,
                 param_min_attendance=10, param_max_attendance=20, param_teacher=t1)

    c1.display()
