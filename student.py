import datetime

# lambda function for eliminating space at the beginning of string
remove_starting_space = lambda param: param[1:] if param[0] == " " else param


class Student:
    def __init__(self, param_date: datetime, param_name: str, param_surname: str, param_id: str, param_tel: str,
                 param_email: str, param_wished_courses: str):
        """
        Constructor for Student class
        :param param_date: date of admission form completion
        :param param_name: name of attendee
        :param param_surname: surname of attendee
        :param param_id: ID of attendee
        :param param_tel: telephone of attendee
        :param param_email: email of attendee
        :param param_wished_courses: text with wished courses
        """
        self.date = param_date
        self.name = param_name
        self.surname = param_surname
        self.ID = param_id
        self.tel = param_tel
        self.email = param_email
        # we get a string that represents the list of wanted courses:
        self.courses = dict()
        # parse text to obtain courses
        tmp = param_wished_courses.split(",")
        for element in tmp:
            self.courses[remove_starting_space(element)] = False

        self.nr_h_week_actual = 0
        self.max_h_week = 20

    def display(self) -> None:
        """
        Prints information about the Student object
        :return: None
        """
        print("Date:", self.date)
        print("Name:", self.name)
        print("Surname:", self.surname)
        print("Id:", self.ID)
        print("Telephone:", self.tel)
        print("Email:", self.email)
        print("Courses:", self.courses)
        print("Nr_h_week_actual:", self.nr_h_week_actual)
        print("Max_h_week:", self.max_h_week)

    def get_courses(self) -> list:
        """
        :return: The dictionary keys for the courses
        """
        return self.courses.keys()

    def add_course(self, key: str, h_session: int) -> None:
        """
        Activate course for object
        :param key: code of course
        :param h_session: number of hours per session
        :return: None
        """
        self.courses[key] = True
        self.nr_h_week_actual += h_session

    def clear_course(self, key: str, h_session: int) -> None:
        """
        Deactivates course for object
        :param key: code of course
        :param h_session: number of hours per session
        :return: None
        """
        self.courses[key] = False
        self.nr_h_week_actual -= h_session

    def check_h_per_week(self) -> bool:
        """
        :return: True if the objects respects the max number of h per week
        """
        return self.nr_h_week_actual <= self.max_h_week

    def check_course_active(self, key: str) -> bool:
        """
        :param key: Code for course to check
        :return: State of course for student object
        """
        return self.courses[key]

    # TODO add necessary methods


if __name__ == "__main__":
    c1 = Student(param_date=datetime.date(2021, 10, 3), param_name="Tom", param_surname="Hanks",
                 param_id="123456789",
                 param_tel="074562164345", param_email="x.x@x.x", param_wished_courses="PB1, DB1, EB1, CB1")
    c1.display()
