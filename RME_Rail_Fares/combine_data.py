from glob import glob
from datetime import datetime
import sys
import os
import pandas as pd
import pprint as pp

def main():

    dailydatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\'
    appendeddatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\appended_data\\'
    dailydataname = 'RME_data_collected_for*'
    appendeddataname = 'appended_data'
    
    fileextension = '.csv'
    #fileextension = '.xlsx'

    dailydata = get_daily_data(dailydatapath,dailydataname,fileextension)
    appendeddata = get_appended_data(appendeddatapath,appendeddataname,fileextension)
    alldata = combine_daily_and_appended_data(dailydata, appendeddata)


    todaysdate = datetime.now().strftime("%Y_%m_%d")
    alldata.to_csv(appendeddatapath + appendeddataname  +"_for_"+ todaysdate + fileextension)
    

def get_daily_data(filepath, filename, fileextension):
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
                               parse_dates=True
                               )

            dataframes.append(temp)
            
    elif fileextension == '.xlsx':
        for count, file in enumerate(listoffiles,1):
            print(f"Loading {os.path.basename(file)} into memory.")
            print(f"That's {count} out of {numberoffiles}, or {str(int((count/numberoffiles)*100))} percent loaded.\n")
            temp = pd.read_excel(file,
                               dtype=dtypedictionary,
                               header=0,
                               encoding='Windows-1252',
                               parse_dates=True
                               )
            temp.index.rename = 'daily_index'
            dataframes.append(temp)

    else:
        print("file extension not specified correctly")

    #check there are more than one daily file first    
    if numberoffiles > 1:
        alldailydata = pd.concat(dataframes,axis=0,sort=False)

    else:
        alldailydata = dataframes
    


    return alldailydata


def get_appended_data(filepath, filename, fileextension):
    dtypedictionary = {'TOC Criteria':str,'Origin':str,'Origin_Code':str,'Destination':str,'Destination_Code':str,'Date_accessed':str,'Time_searched_against':str,'Departure_Gap':str,
                     'Departure_Date':str,'Arrival_time':str,'Duration':str, 'Changes':int,'Price':float,'Fare_Route_Description':str,'Fare_Provider':str,'TOC_Name':str,
                     'TOC_Provider':str,'Ticket_type':str,'nre_fare_category':str,'Duplicate':bool}
    
    df = pd.read_csv(filepath + filename + fileextension,
                               dtype=dtypedictionary,
                               header=0,
                               encoding='Windows-1252',
                               parse_dates=True
                     )
    
    return df

def combine_daily_and_appended_data(dailydata, appendeddata):
    all_data = appendeddata.append(dailydata,ignore_index=True)
    print(all_data.info())
    print(all_data.head(10))
    return all_data




if __name__ == '__main__':
    main()


