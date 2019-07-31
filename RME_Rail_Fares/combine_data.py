from glob import glob
from datetime import datetime
import sys
import os
import pandas as pd
import pprint as pp

def main():

    dailydatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\'
    combineddatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\appended_data\\'
    dailydataname = 'RME_data_collected_for*'
    combineddataname = 'appended_data'
    #fileextension = '.csv'
    fileextension = '.xlsx'

    combine_data(dailydatapath,dailydataname,fileextension)


def combine_data(filepath, filename, fileextension):
    print(filepath,filename,fileextension)
    

    #this is a list f strings
    listoffiles = glob(f'{filepath+filename+fileextension}')
    
    numberoffiles = len(listoffiles)

    print(f"{numberoffiles} {fileextension} files need to be collated") 
    print(f"reading in {fileextension} files from {filepath}")

    dataframes = []
    dtypedictionary = {'TOC Criteria':str,'Origin':str,'Origin_Code':str,'Destination':str,'Destination_Code':str,'Date_accessed':str,'Time_searched_against':str,'Departure_Gap':str,
                     'Departure_Date':str,'Arrival_time':str,'Duration':str, 'Changes':int,'Price':float,'Fare_Route_Description':str,'Fare_Provider':str,'TOC_Name':str,
                     'TOC_Provider':str,'Ticket_type':str,'nre_fare_category':str,'Duplicate':bool}


    if fileextension == '.csv':
        for count, file in enumerate(listoffiles,1):
            print(f"Loading {os.path.basename(file)} into memory.")
            print(f"That's {count} out of {numberoffiles}, or {str(int((count/numberoffiles)*100))} percent loaded.\n")
            temp = pd.read_csv(file,
                               dtype=dtypedictionary,
                               header=0,
                               encoding='Windows-1252',
                               parse_dates=True)

            dataframes.append(temp)

    elif fileextension == '.xlsx':
        for count, file in enumerate(listoffiles,1):
            print(f"Loading {os.path.basename(file)} into memory.")
            print(f"That's {count} out of {numberoffiles}, or {str(int((count/numberoffiles)*100))} percent loaded.\n")
            temp = pd.read_excel(file,
                               dtype=dtypedictionary,
                               header=0,
                               encoding='Windows-1252',
                               parse_dates=True)

            dataframes.append(temp)

    else:
        print("file extension not specified correctly")

    print(dataframes[0].info())
    print(len(listoffiles))



if __name__ == '__main__':
    main()


