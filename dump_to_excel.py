import os

import xlsxwriter
import classrooms


def dump_to_excel_room(room: classrooms.Classrooms, number_weeks: int) -> bool:
    """
    Transform classrooms object in a excel file
    :param room: classrooms object
    :param number_weeks: number of weeks
    :return: True if excel file was created successfully
    """
    # Workbook() takes one, non-optional, argument
    # which is the filename that we want to create.
    file_name = os.path.join(os.getcwd(), 'schedule', 'room_' + room.name + '.xlsx')
    workbook = xlsxwriter.Workbook(file_name)

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    for week in range(number_weeks):
        worksheet = workbook.add_worksheet(name="week_" + str(week))
        # write columns heads
        worksheet.write('A1', 'Hours')
        worksheet.write('B1', 'Monday')
        worksheet.write('C1', 'Tuesday')
        worksheet.write('D1', 'Wednesday')
        worksheet.write('E1', 'Thursday')
        worksheet.write('F1', 'Friday')
        # start from line 2 and go 12 hours
        for line in range(13):
            # write line meanings
            worksheet.write('A' + str(line + 2), '{:2}:00'.format(str(line + 8)))
            # write each day's schedule
            worksheet.write('B' + str(line + 2), str(room.Monday[line]).replace('INV', ''))
            worksheet.write('C' + str(line + 2), str(room.Tuesday[line]).replace('INV', ''))
            worksheet.write('D' + str(line + 2), str(room.Wednesday[line]).replace('INV', ''))
            worksheet.write('E' + str(line + 2), str(room.Thursday[line]).replace('INV', ''))
            worksheet.write('F' + str(line + 2), str(room.Friday[line]).replace('INV', ''))

    # Finally, close the Excel file
    # via the close() method.
    workbook.close()

    if os.path.exists(file_name):
        return True
    else:
        return False


if __name__ == "__main__":
    # dump data to test
    s1 = classrooms.Classrooms(param_name="1", param_capacity=20, param_monday="10:00-14:00", param_tuesday="15:00-20:00",
                               param_wednesday="8:00-14:00",
                               param_thursday="", param_friday="15:00-20:00")

    s1.Friday = ['INV', 'INV', 'DT1_8', 'DT1_9', 'DT2_10', 'DT2_11', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV']
    s1.Monday = ['PB3_7', 'PB3_7', 'DT1_8', 'DT1_9', 'DT2_10', 'DT2_11', 'FREE', 'FREE', 'FREE', 'FREE', 'FREE', 'FREE',
                 'INV']
    s1.Thursday = ['PB3_7', 'PB3_7', 'DT1_8', 'DT1_9', 'DT2_10', 'DT2_11', 'FREE', 'FREE', 'FREE', 'FREE', 'FREE',
                   'FREE', 'INV']
    s1.Tuesday = ['INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'PB3_7', 'PB3_7', 'INV']
    s1.Wednesday = ['INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV', 'INV']

    s1.display()
    dump_to_excel_room(s1, 13)
