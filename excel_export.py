import database_comm
import pymogo
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

    def write_data(self, name, chip_id: str):

        workbook = xlsxwriter.Workbook(name + '.xlsx')
        worksheet = workbook.add_worksheet() # can name the worksheet

        # get data from database_comm
        time = None
        voltage = None
        calculated_capcitance = None
        humidity = None
        temp = None

        # data to write to worksheet
        data = (
            ['Time', 1000], # replace with variable
            ['Voltage', 127],
            ['Calculated Capacitance', 300],
            ['Humidity', 50],
            ['Temp', 25],
        )

        row = 0
        col = 0

        # iterate over data and write it out row by row
        for variable, data in (data):
            # worksheet.write(row, col, some_data)
            worksheet.write(row, col, variable)
            worksheet.write(row, col + 1, data)
            row += 1

        workbook.close()
