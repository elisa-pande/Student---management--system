"""
This module should process the files that describe the possible courses
The folder where this modules looks for the files is courses folder
"""
import os
from docx import Document
import json

# lambda function for eliminating space at the beginning of string
remove_starting_space = lambda param: param[1:] if param[0] == " " else param


def get_files(location: str) -> list:
    """
    Retrieves all the file names from the folder
    :param location: absolute location
    :return: list of strings representing the files
    """
    list_files = []

    for root, dirs, files in os.walk(location):
        for name in files:
            list_files.append(os.path.join(root, name))

    return list_files


def read_file(file_path: str) -> dict:
    """
    Read a file a gather's the information needed for creating the json files.
    :param file_path: file path
    :return: diction with all the information needed for later for creating a json
    """
    # link the variable to the docs document
    file_content = Document(file_path)
    # get all the paragraphs
    file_content = file_content.paragraphs
    # get all the text from paragraphs
    d = dict()
    # get the text of each paragraph and format the text to get the desired information
    # second paragraph contains the name
    d['name'] = remove_starting_space(file_content[1].text.split(':')[-1])
    # third paragraph contains the short name
    d['code'] = remove_starting_space(file_content[2].text.split(':')[-1])
    # 4th paragraph contains the total number of h for course
    d['total_h'] = remove_starting_space(file_content[3].text.split(':')[-1])
    # 5th paragraph contains the total number of hours per session
    d['week_h'] = remove_starting_space(file_content[4].text.split(':')[-1])
    # 6th paragraph contains the number of h per session
    d['session_h'] = remove_starting_space(file_content[5].text.split(':')[-1])
    # 7th paragraph contains the minim number of participants
    d['min_part'] = remove_starting_space(file_content[6].text.split(':')[-1])
    # 8th paragraph contains the maxim number of participants
    d['max_part'] = remove_starting_space(file_content[7].text.split(':')[-1])
    # 9th paragraph contains the tutors of the course
    d['tutors'] = remove_starting_space(file_content[8].text.split(':')[-1])
    # 11th paragraph contains the description
    d['description'] = remove_starting_space(file_content[10].text)

    return d


def course_file_processing(input_folder_path: str, debug=False) -> str:
    """
    This is the main function of the module.
    This function will:
     1. parse the folder where the courses are.
     2. parse each file and retrieve the date
     3. create the courses list for admission
     4. create a json file with all the information gathered in the files
    :param input_folder_path: relative path to folder where the files are
    :param debug: if we want to print debug information to console
    :return: string with abbreviations from all the found courses.
             None if something went wrong.
    """
    return_value = ""

    # get list of files in the folder
    location = os.path.join(os.getcwd(), input_folder_path)
    list_files = get_files(location)

    if debug:
        print("DEBUG: Get files return value: ", list_files, '\n', '_' * 20)

    # variable to hold the name for the json file
    try:
        json_file = open("courses.json", 'w')
    except IOError as e:
        print("ERROR %s: File does not appear to exist.", e.filename)

    # variable to hold the dict elements
    dict_list = []

    # read each file from folder
    for file in list_files:
        # get data from docs and create a dictionary
        dictionary_element = read_file(file)
        # append information to string with abbreviations
        return_value += dictionary_element['cod'] + " - " + dictionary_element["name"] + "\n"
        # append element to list
        dict_list.append(dictionary_element)

        if debug:
            print("DEBUG: Data gathered from ", file, " :", dictionary_element, '\n', '_' * 20)

    # dump to specific json file of the data
    json.dump(dict_list, json_file)

    if debug:
        print("DEBUG: String for abbreviation: ", return_value, '\n', '_' * 20)

    # close the json file
    json_file.close()

    return return_value


if __name__ == "__main__":
    # we use main for local testing of module
    pass
