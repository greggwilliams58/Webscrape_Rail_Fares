import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
import calendar
from collections import defaultdict
import csv
import pandas as pd
import collections
import time
import random
import sys
import os


def main():
    
    #test for live or frozen running
    if getattr(sys,'frozen',False):
        print("running in a bundle\n")
    else:
        print("running live")
    
    frozen = 'not'

    #test for live or frozen with path file info
    if getattr(sys, 'frozen', False):
            # we are running in a bundle
            frozen = 'ever so'
            bundle_dir = sys._MEIPASS
    else:
            # we are running in a normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
    
    print( 'we are',frozen,'frozen')
    print( 'bundle dir is', bundle_dir )
    print( 'sys.argv[0] is', sys.argv[0] )
    print( 'sys.executable is', sys.executable )
    print( 'os.getcwd is', os.getcwd() )
    

    #file paths to be used when working at home
    #routesandtimedata = 'C:\\Users\\gregg_000\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\route_and_time_metadata.xlsx'
    #filepath = 'C:\\Users\\gregg_000\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\'

    #input datafile location and data output location
    routesandtimedatafile = '\\2_Route_and_times_metadata\\route_and_time_metadata.xlsx'
    outputfilepath = '\\3_Data_goes_here\\'
    

    #collect route and times metadata
    alltimesdates = gettingquerydata(resource_path(routesandtimedatafile))
    
    #check day of the week
    dayofexecution = calendar.day_name[datetime.today().weekday()]

    #decide if weekend data collection is needed
    #handler of bank holiday mondays and Xmas may be needed here
    if dayofexecution == "Friday":
        createdataset(resource_path(outputfilepath),alltimesdates)
        for i in range(1,3):
            createdataset(resource_path(outputfilepath),alltimesdates,i)
    else:
        createdataset(resource_path(outputfilepath),alltimesdates)

    #keep the console window open
    input("Press enter to exit after this ;)")


def createdataset(filepath,alltimesdates,datetooffset=0):
    """
    This is the main co-ordinating function of the code.  It generates a series of routes with dates and times to check,
    generates URL, processes the return data and converts it to CSV.

    Parameters:
    filepath:       A string directing where the final output will be saved
    alltimesdata:   A pandas dataframe holding route and times metadata
    datetooffset:   An integer indicating whether the base date shold be incremented or not.  Default is 0

    Returns:
    None
    BUT saves a CSV file with final data at filepath location.
    """
    
    formatted_date = pd.to_datetime(datetime.now()+timedelta(days = datetooffset)).strftime('%d_%m_%Y')
    
    filename = f'RME_data_collected_for_{formatted_date}.csv'#generated the sets of dates and times to work with
    downddatesandtime, updatesandtime = getdatetimesinfo(alltimesdates,datetooffset)
    #pp.pprint(collateddatesandtime)
    #generate the URL's to be processed by NRE website
    urlstoprocess = generateurl(downddatesandtime, updatesandtime)
        
    print(f"getting NRE data for the collection date of {formatted_date} now...")

    #extracting the data from the webset and converting to json
    jsondata = extractwebdata(urlstoprocess)

    #convert the json into csv format and saving it externally as excel xlsx file
    processjson(jsondata,filepath,filename)


def extractwebdata(urlstr):
    """
    This makes a request to the NRE webset and parses the html, selecting the relevant journey data as json format
    it also adds the travel date to the json dataset

    Parameters 
    urlstr:         A list of urls to be used to interrogate the NRE website

    Returns:
    rawjsondata     A list of json-formatted journey information 
    """
    
    rawjsondata=[]
    for counter, items in enumerate(urlstr,1):
        
        randsleep = random.randrange(10,99)/100
        
        print(f"getting item {counter} of {len(urlstr)} with a pause of {randsleep} seconds")

        try:

            response = urllib.request.urlopen(items[1])
            time.sleep(randsleep)

        except OSError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(f"{e}\n"))
            print(f"The url used was {items[1]}")   
        except urllib.error.URLError as URLwrong:
            print(f"The URL is wrong.  The error code is {URLwrong.code}. Check this error code against https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.responses \n")  
            print(f"The reason given for the error is: {URLwrong.reason} \n")
            print(f"The url used was {items[1]}")
        except urllib.error.HTTPError as HTTPwrong:
            print(f"HTTP is wrong. The error code is {HTTPwrong.code}. Check this error code against https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.responses")
            print(f"The reasons given for the error is {HTTPwrong.reason} \n")
            print(f"The url used was {items[1]}")
        except TimeoutError as e:
            print(str(e))
            print("OOPS!! Timeout Error.  Check that the URL is correct.\n")
            print(f"The url used was {items[1]}")




        soup = BeautifulSoup(response,'html.parser')

        #extract the required json data
        if soup.find('script',{ 'id':f'jsonJourney-4-1' }) is not None:
            td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text
        else:
            pass
        #convert the json data into a dictionary
        jsonData = json.loads(td_class)

        #add the search data information to the json data
        
        jsonData['jsonJourneyBreakdown'].update(TravelDate = items[1][61:67])
        jsonData['jsonJourneyBreakdown'].update(TOCSearchCriteria = items[0])    
        
        filledtime = items[2].zfill(4)
        formattedtime = filledtime[:2]+ ":" + filledtime[2:]
        jsonData['jsonJourneyBreakdown'].update(TimeSearchedFor = formattedtime) 
        
        rawjsondata.append(jsonData)
  
            
    return rawjsondata


def processjson(jsoninfo,fp, fn):
    """
    This converts the json formatted data into CSV and exports it to a specified location

    Parameters
    jsoninfo:   A list of json-formatted data
    fp:         A string of the file path to where the data is exported
    gn:         A string with the name of the file to be exported

    Returns:
    None,
    but a csv file is exported
    """

    print("preparing the csv file")
    #initialisation information
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    response_header = list()

    #create a blank csv object
    datafile = open(fp + fn, 'w',newline='')
    
    #create a csvwriter object
    csvwriter = csv.writer(datafile)

    #create a header for the csv file
    
    response_header.append('TOC Criteria')
    response_header.append('Origin')
    response_header.append('Origin_Code')
    response_header.append('Destination')
    response_header.append('Destination_Code')
    response_header.append('Date_accessed')
    response_header.append('Time_searched_against')
    response_header.append('Departure_Gap')
    response_header.append('Departure_Date')
    response_header.append('Departure_Day')
    response_header.append('Departure_time')
    response_header.append('Arrival_time')
    response_header.append('Duration')
    response_header.append('Changes')
    response_header.append('Price')

    response_header.append('Fare_Route_Description')
    response_header.append('Fare_Provider')
    response_header.append('TOC_Name')
    response_header.append('TOC_Provider')
    response_header.append('Ticket_type')
    response_header.append('nre_fare_category')


    #write the csv header row
    csvwriter.writerow(response_header)

    #extract data from the json file
    response = []
    for journey in jsoninfo:
        response.append(journey['jsonJourneyBreakdown']['TOCSearchCriteria'])
        response.append(journey['jsonJourneyBreakdown']['departureStationName'])
        response.append(journey['jsonJourneyBreakdown']['departureStationCRS'])
        response.append(journey['jsonJourneyBreakdown']['arrivalStationName'])
        response.append(journey['jsonJourneyBreakdown']['arrivalStationCRS'])
        #derived formatted date for date of data extraction
        todaydate = datetime.now()
        response.append(todaydate.strftime('%Y%m%d_%H-%M'))
        response.append(journey['jsonJourneyBreakdown']['TimeSearchedFor'])
        #get and format date of travel
        traveldate = str(journey['jsonJourneyBreakdown']['TravelDate'])
        
        #add / marks to avoid excel formatting doing odd things
        traveldate = traveldate[0:2] + '/' + traveldate[2:4] + '/' + traveldate [4:6]
        
        #placeholder for 'Departure_Days_Ahead'
        timedelta_gap = (datetime.strptime(traveldate,"%d/%m/%y") - todaydate)+timedelta(days=1)
        
        travel_gap = timedelta_gap.days
        
        response.append(travel_gap)

        #add the formatted travel date to list
        response.append(traveldate)

        #departure day
        response.append(weekdays[datetime.strptime(traveldate,"%d/%m/%y").weekday()])

        response.append(journey['jsonJourneyBreakdown']['departureTime'])
        response.append(journey['jsonJourneyBreakdown']['arrivalTime'])

        #journey_duration
        travel_time = str(journey['jsonJourneyBreakdown']['durationHours']) + ":" + str(journey['jsonJourneyBreakdown']['durationMinutes'])

        response.append(travel_time)
        response.append(journey['jsonJourneyBreakdown']['changes'])
        response.append(journey['singleJsonFareBreakdowns'][0]['ticketPrice'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareRouteDescription'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareProvider'])
        response.append(journey['singleJsonFareBreakdowns'][0]['tocName'])
        response.append(journey['singleJsonFareBreakdowns'][0]['tocProvider'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareTicketType'])
        response.append(journey['singleJsonFareBreakdowns'][0]['nreFareCategory'])
        

        #write data to the row of the csv file
        csvwriter.writerow(response)

        #flush the list to prepare for the next row
        response = []

    #close the file and export the data
    csv_data = datafile.close()
    

    #convert into a dataframe
    df_data = pd.read_csv(fp + fn)

    #identify duplicates
    df_data['Duplicate']= df_data.duplicated(subset=['TOC Criteria','Origin','Origin_Code','Destination','Destination_Code','Date_accessed','Time_searched_against','Departure_Gap','Departure_Date','Departure_Day','Departure_time','Arrival_time','Duration','Price','Fare_Route_Description'],keep='first')

    #legacy code to export file as excel
    #df_data.to_excel(fp + fn.replace('csv','xlsx'))
    df_data.to_csv(fp+fn)
    
def generateurl(downinfo,upinfo):
    """
    This generates a list of urls based on provided date,route and time information, which are then fed to the NRE website

    Parameters:
    collecteddateinfo:  a default dictionary {dateoftravel:[[up journey],[times],[down journey],[times]]}

    Returns:
    urltoprocess:       a list containting travel date and url information [traveldate, url]
    """
    
    
    combinedupanddownurls = {}
    urldown = []
    urlup = []

    #walk through dates, routes and times to create url
    for trip in upinfo:

        if trip[4] == 'All TOCs':
            #print(f"The time interator object is {trip[3]}")
            for tcounter,times in enumerate(trip[3],0):
                #print(f"The individual time interator object is {trip[3][tcounter]}")
                url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly'  
                
                if "//dep" in url:
                    print(f"No times supplied for time {trip[3]} and {url}")
                else:
            
                    urldown.append([trip[4],url,trip[3][tcounter]])
                    print(url)
            #check if times have been supplied from the metadata
        else:
            for tcounter,times in enumerate(trip[3],0):
                url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly&show='+trip[4]                    
            #check if times have been supplied from the metadata

                if "//dep" in url:
                    print(f"No times supplied for time {trip[3]} and {url}")
                else:
            
                    urldown.append([trip[4],url,trip[3][tcounter]])
                    print(url)
                  

    for trip in downinfo:

        if trip[4] == 'All TOCs':
            for tcounter,times in enumerate(trip[3],0):
                url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly'                    
            #check if times have been supplied from the metadata
            
                if "//dep" in url:
                    print(f"No times supplied for time {trip[3]}: {url}")
                else:
                    urldown.append([trip[4],url,trip[3][tcounter]])
                    print(url)

        else:
            for tcounter,times in enumerate(trip[3],0):
                url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly&show='+trip[4]                    
            #check if times have been supplied from the metadata

                if "//dep" in url:
                    print(f"No times supplied for time {trip[3]}: {url}")
                else:
                    urldown.append([trip[4],url,trip[3][tcounter]])
                    print(url)




    #combine both up and down routes into a new common list
    combinedupanddownurls = urldown + urlup
    
    return combinedupanddownurls
        
  
def getdatetimesinfo(routesandtimes, dateoffset):
    """
    This is an 'initialisation' procedure which sets most of the parameters for the functioning of the whole process.
    It takes a date and derives the dates 1,7 and 30 days in the future and then dertives the appropriate days, origin and destination routes and departure times for each of these factors
    
    Parameters:
    routesandtimes: A dataframe holding routes and times information
    dateoffset:     An integer representing the number of days to alter the date of search by.  DEFAULT is 0 days

    Returns:
    datesandtimes:  A default dictionary containing {dateoftravel+startstationcode:[[up journey],[times],[down journey],[times]]}

    """
    #ok here
    #pp.pprint(routesandtimes)
    
    #increment date to check if needed
    datetocheck = datetime.today()+timedelta(days=dateoffset)
    
    #initialisation information
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    
    #test placeholder for beth's 1-30 days
    #daystomoveahead = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    daystomoveahead = [1,7,30]
    #populate defaultdict with values depending on date increments day of the week
    
    downdatesandtimes = list()
    updatesandtimes = list()

    ###start loop with all the dates and times here
    for count, items in enumerate(routesandtimes):
        
        downroute = routesandtimes[count][0][0]
        uproute = routesandtimes[count][0][1]
        downweekdaytimes = routesandtimes[count][1]
        downsaturdaytimes = routesandtimes[count][2]
        downsundaytimes = routesandtimes[count][3]

        upweekdaytimes = routesandtimes[count][4]
        upsaturdaytimes = routesandtimes[count][5]
        upsundaytimes = routesandtimes[count][6]
        
        toc_filter = routesandtimes[count][7]
        
            
        #for each date to move ahead increment
        for counter,item in enumerate(daystomoveahead):

            futuredate = datetocheck + timedelta(daystomoveahead[counter])

            formattedfuturedate, dayofweek = futuredate.strftime('%d%m%y'), weekdays[futuredate.weekday()]


            #derive day of week from date
            daycheck = weekdays[futuredate.weekday()]
            if daycheck in ("Monday","Tuesday","Wednesday","Thursday","Friday"):
                daytocheck = 'weekday'
                downtimestocheck = downweekdaytimes
                uptimestocheck = upweekdaytimes
            elif daycheck in ("Saturday"):
                daytocheck = 'saturday'
                downtimestocheck = downsaturdaytimes
                uptimestocheck = upsaturdaytimes
            elif daycheck in ("Sunday"):
                daytocheck = 'sunday'
                downtimestocheck = downsundaytimes
                uptimestocheck = upsundaytimes
            else:
                print("error")

            
            downdatesandtimes.append(["downroute",formattedfuturedate,downroute,downtimestocheck,toc_filter])
            updatesandtimes.append(["uproute",formattedfuturedate, uproute,uptimestocheck,toc_filter])
    
    return downdatesandtimes,updatesandtimes


def gettingquerydata(fp):
    """
    This reads in route and time table information from an excel file. It also converts this excel data into a list of lists to be plugged into
    the function gettimesdatesinfo.

    Parameters:
    fp: a string containing the filepath of the data file holding route and time info

    Returns:
    a list of list with 
    """
    
    raw_data = pd.read_excel(fp)

    del raw_data['variable name']

    final_list = []
    temp_list = []
    
    for count, items in enumerate(raw_data):
        
        routesup = raw_data.iloc[1,count].split(',') 
        routesdown = raw_data.iloc[2,count].split(',')
    
        routes = [routesup, routesdown]
        temp_list.append(routes)

        
        downweekdaytime = raw_data.iloc[3,count].split(',')
        temp_list.append(downweekdaytime)
    
        

        downsaturdaytime = raw_data.iloc[4,count].split(',')
        temp_list.append(downsaturdaytime)

        

        downsundaytime = raw_data.iloc[5,count].split(',')
        temp_list.append(downsundaytime)

        upweekdaytime = raw_data.iloc[6,count].split(',')
        temp_list.append(upweekdaytime)

        upsaturdaytime = raw_data.iloc[7,count].split(',')
        temp_list.append(upsaturdaytime)

        upsundaytime = raw_data.iloc[8,count].split(',')
        temp_list.append(upsundaytime)

        toc_filter = raw_data.iloc[0,count]
        temp_list.append(toc_filter)

        final_list.append(temp_list)

        temp_list = []

    

    return final_list


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds


def resource_path(relativepath):
    """
    Redirection of approot path based on whether the application is bundled into an .exe file or not

    Parameters:
    relativepath    A string giving the rest of the path to the required resource

    Returns
    fullpath        A string containing the right root and relative path
    """
    
    fullpath = ''

    if getattr(sys, 'frozen',False):
        fullpath = sys._MEIPASS + relativepath
    else:
        fullpath = os.path.dirname(os.path.abspath(__file__)) + relativepath
    
    return fullpath

#routine boilerplate
if __name__ == '__main__':
    main()