from glob import glob
from datetime import datetime
import sys
import os
import pandas as pd
import pprint as pp

def main():
    """
    This serves the purpose of appending daily data to a combined dataset
    """
    dailydatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\'
    appendeddatapath = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\3_Data_goes_here\\appended_data\\'
    dailydataname = 'RME_data_collected_for*'
    appendeddataname = 'appended_data'
    
    fileextension = '.csv'
    #fileextension = '.xlsx'

    dailydata = get_daily_data(dailydatapath,dailydataname,fileextension)
    appendeddata = get_appended_data(appendeddatapath,appendeddataname,fileextension)
    
    #alldata = combine_daily_and_appended_data(dailydata, appendeddata)


    #todaysdate = datetime.now().strftime("%Y_%m_%d")
    #alldata.to_csv(appendeddatapath + appendeddataname  +"_for_"+ todaysdate + fileextension)
    
    #cleanup(todaysdate)


def get_daily_data(filepath, filename, fileextension):
    """
    This finds the daily dataset file and loads it into a dataframe, with data conversion.  If there are more than one datasets in the folder, all datasets will be concatinated.
    It can handle csv or xslx formats

    Parameters:
    filepath:       A string containing a filepath 
    filename:       A string containing the filename to be loaded
    fileextension:  A string containing a file extension.  Only ".xlsx" and ".csv" are handled

    Output:
    alldailydata:   A data frame holding the daily dataset
    """
    #print(filepath,filename,fileextension)
    

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
    """
    This identifies the latest file from the appended folder and loads that file into a dataframe

    Parameters:
    filepath:       A string containing the filepath to the appended data folder
    filename:       A string containing the generic name of the appended file
    fileextension:  A string containing the file extension.  Only csv is currently supported

    Returns
    df:             A df containing the appended dataset

    """
    list_of_files = glob(filepath +'*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
   
    dtypedictionary = {'TOC Criteria':str,'Origin':str,'Origin_Code':str,'Destination':str,'Destination_Code':str,'Date_accessed':str,'Time_searched_against':str,'Departure_Gap':str,
                     'Departure_Date':str,'Arrival_time':str,'Duration':str, 'Changes':int,'Price':float,'Fare_Route_Description':str,'Fare_Provider':str,'TOC_Name':str,
                     'TOC_Provider':str,'Ticket_type':str,'nre_fare_category':str,'Duplicate':bool}
    
    df = pd.read_csv(latest_file,
                               dtype=dtypedictionary,
                               header=0,
                               encoding='Windows-1252',
                               parse_dates=True
                     )
    print(df.info())
    return df

def combine_daily_and_appended_data(dailydata, appendeddata):
    """
    This appends the 
    """

    all_data = pd.concat([appendeddata,dailydata],ignore_index=True,sort=False) 
    
    all_data.rename_axis('General_index', axis = 'index', inplace=True)

    all_data.rename(columns={'Unnamed: 0':'load_index'}, inplace=True)

    all_data.set_index(['load_index'],append=True,inplace=True)
    print(all_data.info())


    return all_data

def cleanup():
    pass



if __name__ == '__main__':
    main()


