import database_comm
import pymongo
import xlsxwriter

class Exporter:
    
    '''
    Class definition for the Excel Exporter. 
    TODO: Complete code based off example code and complete
    based on our use case. 
    '''

    '''
    TODO: Finish initializer to get all the variables and/or communicators
    to get data from the database from a specific die
    '''
    # def __init__(self, chip_id: int) -> None:
    #     self.chip_id = chip_id
    #     workbook = xlsxwriter.Workbook('hello.xlsx')

    def write_data(self, chip_id: str, test_num: int): # test_num -1 if all tests requested

        workbook = xlsxwriter.Workbook(chip_id + '.xlsx')  

        if test_num == -1: # if all tests are wanted
            for i in range(test_num):

                worksheet = workbook.add_worksheet(test_num) # worksheet is named by test number

                sweeps = get_die_sweeps(chip_id, test_num)

                worksheet.write('A1', 'Chip ID: ' + chip_id)
                worksheet.write('B1', 'Test Number' + test_num)

                for sweep in (sweeps):

                   # get data from database_comm
                    time = sweep[2]
                    humidity = sweep[3]
                    voltage = sweep[4]
                    capacitance = sweep[5]
                    temp = sweep[6]

                    # data to write to worksheet
                    data = (
                        ['Time', time],
                        ['Humidity', humidity],
                        ['Voltage', voltage],
                        ['Calculated Capacitance', capacitance],
                        ['Temp', temp],
                    )

                    row = 1
                    col = 0

                    # iterate over data and write it out row by row
                    for variable, data in (data):
                        # worksheet.write(row, col, some_data)
                        worksheet.write(row, col, variable)
                        worksheet.write(row, col + 1, data)
                        row += 1

                test_num += 1 #increase the test number to look at the next test
            
            workbook.close()

        else: # if only one specific test is wanted

            worksheet = workbook.add_worksheet() # can name the worksheet

            sweeps = get_die_sweeps(chip_id, test_num)

            worksheet.write('A1', 'Chip ID: ' + chip_id)
            worksheet.write('B1', 'Test Number' + test_num)

            for sweep in (sweeps):

                   # get data from database_comm
                    time = sweep[2]
                    humidity = sweep[3]
                    voltage = sweep[4]
                    capacitance = sweep[5]
                    temp = sweep[6]

                    # data to write to worksheet
                    data = (
                        ['Time', time],
                        ['Humidity', humidity],
                        ['Voltage', voltage],
                        ['Calculated Capacitance', capacitance],
                        ['Temp', temp],
                    )

                    row = 1
                    col = 0

                    # iterate over data and write it out row by row
                    for variable, data in (data):
                        # worksheet.write(row, col, some_data)
                        worksheet.write(row, col, variable)
                        worksheet.write(row, col + 1, data)
                        row += 1
                
            workbook.close()
