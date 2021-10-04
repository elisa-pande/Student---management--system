import os

# lambda function for printing format
format_element = lambda x: "    " if x == 'CLASS' else (x + " " if x != 'FREE' else x)


class Classrooms:
    def __init__(self, param_name: str, param_capacity: int, param_monday: str, param_tuesday: str,
                 param_wednesday: str, param_thursday: str, param_friday: str):
        """
        Constructor for classrooms objects
        :param param_name: name of room
        :param param_capacity: capacity of the room
        :param param_monday: list for schedule for Monday
        :param param_tuesday: list for schedule for Tuesday
        :param param_wednesday: list for schedule for Wednesday
        :param param_thursday: list for schedule for Thursday
        :param param_friday: list for schedule for Friday
        """
        self.name = param_name
        self.capacity = param_capacity
        self.Monday = self.transform_text_to_list_availability(param_monday)
        self.Tuesday = self.transform_text_to_list_availability(param_tuesday)
        self.Wednesday = self.transform_text_to_list_availability(param_wednesday)
        self.Thursday = self.transform_text_to_list_availability(param_thursday)
        self.Friday = self.transform_text_to_list_availability(param_friday)

    @staticmethod
    def transform_text_to_list_availability(available: str) -> list:
        """
        Transform string to list of schedule format
        :param available: string data
        :return: list of schedule
        """
        # create a list of availability
        #        8:00   9:00  10:00  11:00  12:00  13:00  14:00  15:00  16:00  17:00  18:00  19:00  20:00
        slot_list = ['CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS', 'CLASS']

        if available is not "":
            # we get string like this for example: 10:00-14:00
            # we want to split it in a list like this for example: ['10:00', '14:00']
            tmp = available.split("-")
            # print(tmp)
            # we want get the int value of the starting h interval: starting h is at position 0 then we split the string at
            # ":" and take again the first position
            start = int(tmp[0].split(":")[0])
            # we want get the int value of the ending h interval: starting h is at position -1 then we split the string at
            # ":" and take again the first position
            end = int(tmp[-1].split(":")[0])
            # transition of h value to position
            start_position = start - 8
            end_position = end - 8
            # print(start_position, end_position)

            for element in range(start_position, end_position, 1):
                slot_list[element] = 'FREE'
            # print(list)

        return slot_list

    @staticmethod
    def get_free_slots(slot_list: list) -> int:
        """
        :param slot_list: list with schedule format
        :return: the number of free slots
        """
        return slot_list.count('FREE')

    @staticmethod
    def is_cod_slots(slot_list: list, cod: str) -> int:
        """
        :param slot_list: list with schedule format
        :param cod: code of abbreviation
        :return: The number of occurs of the code in the list
        """
        return slot_list.count(cod)

    @staticmethod
    def add__slots(slot_list: list, abbrev: str, slots: int) -> list:
        """
        Add slots in the list with the proper abbreviation
        :param slot_list: List with schedule format
        :param abbrev: Code of abbreviation
        :param slots: Number of slots to add
        :return: New list with added data
        """
        start_index = slot_list.index('FREE')
        end_index = start_index + slots
        for i in range(start_index, end_index):
            slot_list[i] = abbrev

        return slot_list

    def display(self) -> None:
        """
        Prints information about the classrooms object
        :return: None
        """
        print("Name: ", self.name)
        print("Capacity: ", self.capacity)
        print("Monday: ", self.Monday)
        print("Tuesday: ", self.Tuesday)
        print("Wednesday: ", self.Wednesday)
        print("Thursday: ", self.Thursday)
        print("Friday: ", self.Friday)

    @staticmethod
    def list_to_print(slot_list: list) -> str:
        """
        Converts list of the scheduler into a string
        :param slot_list: Schedule list
        :return: String with the desired format
        """
        string = ""
        for element in [format_element(el) for el in slot_list]:
            string += '{:7}'.format(element)

        return string

    def display_schedule(self) -> None:
        """
        Prints information about the classrooms object
        :return: None
        """
        print("Name: ", self.name)
        print('{:15}'.format("Hours: "),
              "08:00  09:00  10:00  11:00  12:00  13:00  14:00  15:00  16:00  17:00  18:00  19:00  20:00")
        print('{:15}'.format("Monday: "), self.list_to_print(self.Monday))
        print('{:15}'.format("Tuesday: "), self.list_to_print(self.Tuesday))
        print('{:15}'.format("Wednesday: "), self.list_to_print(self.Wednesday))
        print('{:15}'.format("Thursday: "), self.list_to_print(self.Thursday))
        print('{:15}'.format("Friday: "), self.list_to_print(self.Friday))
        print('_' * 110)

    def is_free_slots(self, needed_size: int) -> bool:
        """
        :param needed_size:
        :param needed_size: size to inquire
        :return: True if the desired size is free over all schedule of the room
        """
        free = self.get_free_slots(self.Monday) + self.get_free_slots(self.Tuesday) + \
            self.get_free_slots(self.Wednesday) + self.get_free_slots(self.Thursday) + self.get_free_slots(
            self.Friday)

        if needed_size <= free:
            return True
        else:
            return False

    def free_days_per_week(self) -> int:
        """
        :return: the number of free days for the classrooms objects
        """
        days = 0
        if self.get_free_slots(self.Monday) > 0:
            days += 1
        if self.get_free_slots(self.Tuesday) > 0:
            days += 1
        if self.get_free_slots(self.Wednesday) > 0:
            days += 1
        if self.get_free_slots(self.Thursday) > 0:
            days += 1
        if self.get_free_slots(self.Friday) > 0:
            days += 1

        return days

    def add_course_to_classroom(self, cod: str, h_per_session: int) -> bool:
        """
        Add course session in a day of the week from the room
        :param cod: cod abbreviation to add to slots
        :param h_per_session: number of slots to use
        :return: True if slots where added successful
        """
        # check availability each day and prevent multiple sessions in same day
        if self.get_free_slots(self.Monday) >= h_per_session and not self.is_cod_slots(self.Monday, cod):
            self.Monday = self.add__slots(self.Monday, cod, h_per_session)
            return True
        elif self.get_free_slots(self.Tuesday) >= h_per_session and not self.is_cod_slots(self.Tuesday, cod):
            self.Tuesday = self.add__slots(self.Tuesday, cod, h_per_session)
            return True
        elif self.get_free_slots(self.Wednesday) >= h_per_session and not self.is_cod_slots(self.Wednesday, cod):
            self.Wednesday = self.add__slots(self.Wednesday, cod, h_per_session)
            return True
        elif self.get_free_slots(self.Thursday) >= h_per_session and not self.is_cod_slots(self.Thursday, cod):
            self.Thursday = self.add__slots(self.Thursday, cod, h_per_session)
            return True
        elif self.get_free_slots(self.Friday) >= h_per_session and not self.is_cod_slots(self.Friday, cod):
            self.Friday = self.add__slots(self.Friday, cod, h_per_session)
            return True

        return False


def get_classrooms_from_csv(folder_path: str, debug: bool = False) -> list:
    """
    Get the information for classrooms from classrooms.csv and retrieved as a dictionary
    :param folder_path: location of classrooms csv
    :param debug: if you want debug information
    :return: list of dictionaries for each room
    """

    if debug:
        print("DEBUG: folder path for classrooms: ", folder_path, '\n', '_' * 20)

    list_files = []
    # get csv file path
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), folder_path)):
        for name in files:
            csv_file = os.path.join(root, name)
    # read the csv line with line
    with open(csv_file, 'r') as file:
        for line in file:
            # split the line at comma
            line = line.split(',')
            # check if line is not empty
            if line[0] != '':
                dict_element = {}
                dict_element['name'] = line[0]
                dict_element['capacity'] = line[1]
                dict_element['Monday'] = line[2]
                dict_element['Tuesday'] = line[3]
                dict_element['Wednesday'] = line[4]
                dict_element['Thursday'] = line[5]
                dict_element['Friday'] = line[6]
                # get rid of new line character
                dict_element['Friday'] = dict_element['Friday'].replace('\n', '')
                # add element to list
                list_files.append(dict_element)
    # take out the header of the csv file
    list_files = list_files[1:]

    return list_files


if __name__ == "__main__":
    s1 = Classrooms(param_name="1", param_capacity=20, param_monday="10:00-14:00", param_tuesday="15:00-20:00",
                    param_wednesday="8:00-14:00",
                    param_thursday="", param_friday="15:00-20:00")
    s1.display()
    s1.display_schedule()
