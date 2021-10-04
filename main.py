import os

import processing_courses
import admission
import schedule


# Values for option possible
class MENU:
    EXIT = 0
    COURSES_GENERATOR = 1
    START_ENROLLMENT = 2
    ENROLL_STUDENTS = 3
    FINISH_ENROLL = 4
    FINISH_SESSION = 5
    SCHEDULE_GENERATOR = 6

    MENU_IDLE = "1.Generating courses\n0.Exit\nWhat option you want:"
    MENU_PRE_STATE = "1.Generating courses\n2.Start Enrollment\n5.Finish session\n" \
                     "0.Exit\nWhat option you want:"
    MENU_PENDING = "3.Enroll student\n4.Stop Enrollment\n5.Finish session\n" \
                   "0.Exit\nWhat option you want:"
    MENU_START = "6.Generating schedule\n5.Finish session\n0.Exit\n" \
                 "What option you want:"


# state machine states
class STATES:
    IDLE_STATE = 0
    PRE_STATE = 1
    PENDING_STATE = 2
    START_STATE = 3


# config values
FOLDER_COURSES = "courses"
FOLDER_ENROLLMENT = "enrollment"
FOLDER_CLASSROOMS = "classrooms"


def clear_file(path):
    """
    Function for clearing content of files
    :param path: location of file
    :return: None
    """
    # protection against file not found error
    try:
        file = open(path, 'w')
        file.write("")
        file.close()
    except IOError as e:
        print("ERROR %s: File does not appear to exist.", e.filename)


def menu(system_state: int, debug: bool = False) -> int:
    """
    Prints to console the menu and retrieves the desired option
    :param debug: if we want debug information
    :param system_state: the state of the system for proper printing to console
    :return: option chosen by the user
    """
    # variable to hold the necessary text to print for menu option
    text_to_print = ""

    if debug:
        print("DEBUG: System state value in menu: ", system_state, '\n', '_' * 20)

    # get proper text for each system state
    if system_state == STATES.IDLE_STATE:
        text_to_print = MENU.MENU_IDLE
    elif system_state == STATES.PRE_STATE:
        text_to_print = MENU.MENU_PRE_STATE
    elif system_state == STATES.PENDING_STATE:
        text_to_print = MENU.MENU_PENDING
    elif system_state == STATES.START_STATE:
        text_to_print = MENU.MENU_START

    opt = int(input(text_to_print))

    if debug:
        print('_' * 20)
        print("DEBUG: Option selected: ", opt, '\n', '_' * 20)

    return opt


def clear_data():
    """
    Deletes data from an instance of the program
    :return: None
    """
    clear_file("courses_tmp.txt")
    if os.path.exists(os.path.join(os.getcwd(), 'courses.json')):
        os.remove(os.path.join(os.getcwd(), 'courses.json'))
    if os.path.exists(os.path.join(os.getcwd(), FOLDER_ENROLLMENT, 'template_registration.docx')):
        os.remove(os.path.join(os.getcwd(), FOLDER_ENROLLMENT, 'template_registration.docx'))
    if os.path.exists(os.path.join(os.getcwd(), 'student.json')):
        os.remove(os.path.join(os.getcwd(), 'student.json'))


def main(debug=False) -> None:
    """
    Main function of the program
    :return: None
    """
    # get value for state from the last run

    try:
        file = open("main_tmp.txt", 'r')
        state = int(file.read())
        file.close()
    except IOError:
        print("ERROR %s: File does not appear to exist.", IOError.filename)

    if debug:
        print("DEBUG: Start-up state", state, '\n', '_' * 20)

    # continuous run loop
    while True:
        # get the option chosen by the user
        option = menu(state, debug)
        # actions to do before closing the application
        if option == MENU.EXIT:
            # state saved for next run
            try:
                file = open("main_tmp.txt", 'w')
                file.write(str(state))
                file.close()
            except IOError as e:
                print("ERROR %s: File does not appear to exist.", e.filename)

            if debug:
                print("DEBUG: state saved: ", state, '\n', '_' * 20)
            # stop the infinite loop
            break

        # action to do when the session is finalised
        elif option == MENU.FINISH_SESSION:
            # clear the stored data
            clear_data()
            state = STATES.IDLE_STATE

        # actions to do for generating courses step
        elif option == MENU.COURSES_GENERATOR and (state == STATES.PRE_STATE or state == STATES.IDLE_STATE):
            state = STATES.PRE_STATE
            # get string with course options
            data_from_courses = processing_courses.course_file_processing(FOLDER_COURSES, debug)
            # save text for future use in a file
            try:
                file = open("courses_tmp.txt", 'w')
                file.write(str(data_from_courses))
                file.close()
            except IOError as e:
                print("ERROR %s: File does not appear to exist.", e.filename)

        # actions to do when the admission starts
        elif option == MENU.START_ENROLLMENT and state == STATES.PRE_STATE:
            # get information saved in file for submission form
            try:
                file = open("courses_tmp.txt", 'r')
                text = file.read()
                file.close()
                # change admission form
                if admission.modify_registration_form(text, FOLDER_ENROLLMENT, debug):
                    state = STATES.PENDING_STATE
            except IOError as e:
                print("ERROR %s: File does not appear to exist.", e.filename)

        # actions to do when online form is used
        elif option == MENU.ENROLL_STUDENTS and state == STATES.PENDING_STATE:
            # get information saved in file for submission form
            try:
                file = open("courses_tmp.txt", 'r')
                text = file.read()
                file.close()
            except IOError as e:
                print("ERROR %s: File does not appear to exist.", e.filename)
            # run form for adding one person to admission list.
            admission.student_registration(text, debug)

        # actions needed for closing the admission phase
        elif option == MENU.FINISH_ENROLL and state == STATES.PENDING_STATE:
            state = STATES.START_STATE
            # get all admission documents stored
            admission.registration_students_word(FOLDER_ENROLLMENT, debug)

        # actions needed for generating the schedule
        elif option == MENU.SCHEDULE_GENERATOR and state == STATES.START_STATE:
            state = STATES.IDLE_STATE
            # generate schedule
            if schedule.generate_schedule(FOLDER_CLASSROOMS, debug):
                clear_data()
        # visual help to better see on console
        print("*" * 60)

        if debug:
            print("DEBUG: new state: ", state, '\n', '_' * 20)


if __name__ == "__main__":
    main(debug=False)
