# import database_comm
import xlsxwriter

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Hello world')
workbook.close()

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
    def __init__(self, chip_id: int) -> None:
        self.chip_id = chip_id
        workbook = xlsxwriter.Workbook('hello.xlsx')