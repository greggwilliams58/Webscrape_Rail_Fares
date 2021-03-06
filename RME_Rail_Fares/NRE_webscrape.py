import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta, date
import calendar
from collections import defaultdict
import csv
import pandas as pd
import collections
import time
import random
import sys
import os
import combine_data
import numpy as np

def main():
    
    #test for live/source code or frozen/package running
    if getattr(sys,'frozen',False):
        print("running in a bundle\n")
    else:
        print("running live")
    
    frozen = 'not'

    #test for live/source code or frozen/package with path file info
    if getattr(sys, 'frozen', False):
            # we are running in a package
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
    

    #input datafile location and data output location
    routesandtimedatafile = '\\2_Route_and_times_metadata\\route_and_time_metadata.xlsx'
    outputfilepath = '\\3_Data_goes_here\\'
    appendeddatapath = '\\3_Data_goes_here\\appended_data\\'

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
    
    #append daily data to appended file
    combine_data.tidyupfiles(resource_path(outputfilepath), resource_path(appendeddatapath))
    
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
    
    #generate the URL's to be processed by NRE website
    urlstoprocess = generateurl(downddatesandtime, updatesandtime)
        
    print(f"getting NRE data for the collection date of {formatted_date} now...")

    #extracting the data from the webset and converting to json
    jsondata = extractwebdata(urlstoprocess)

    #convert the json into csv format and saving it externally as excel xlsx file
    processjson(jsondata,filepath,filename,datetooffset)


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
        
        jsonData['jsonJourneyBreakdown'].update(SearchType = items[3])

        rawjsondata.append(jsonData)
   
    return rawjsondata


def processjson(jsoninfo,fp, fn,datetooffset):
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
    response_header.append('Search_Type')
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
        response.append(journey['jsonJourneyBreakdown']['SearchType'])
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

        timedelta_gap = (datetime.strptime(traveldate,"%d/%m/%y") - (todaydate+(timedelta(days=datetooffset)))+timedelta(days=1))
        
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
        
        #test for null responses on fare information
        if journey['singleJsonFareBreakdowns']:
            response.append(journey['singleJsonFareBreakdowns'][0]['ticketPrice'])
            response.append(journey['singleJsonFareBreakdowns'][0]['fareRouteDescription'])
            response.append(journey['singleJsonFareBreakdowns'][0]['fareProvider'])
            response.append(journey['singleJsonFareBreakdowns'][0]['tocName'])
            response.append(journey['singleJsonFareBreakdowns'][0]['tocProvider'])
            response.append(journey['singleJsonFareBreakdowns'][0]['fareTicketType'])
            response.append(journey['singleJsonFareBreakdowns'][0]['nreFareCategory'])
        else:
            response.append(float(0.00))
            response.append("missing")
            response.append("missing")
            response.append("missing")
            response.append("missing")
            response.append("missing")
            response.append("missing")

        

        #write data to the row of the csv file
        csvwriter.writerow(response)

        #flush the list to prepare for the next row
        response = []

    #close the file and export the data
    csv_data = datafile.close()
    

    #convert into a dataframe
    df_data = pd.read_csv(fp + fn, index_col=False)
    df_data.reset_index(drop=True,inplace=True)
    
    #identify duplicates
    df_data['Duplicate']= df_data.duplicated(subset=['TOC Criteria','Origin','Origin_Code','Destination','Destination_Code','Date_accessed','Time_searched_against','Departure_Gap','Departure_Date','Departure_Day','Departure_time','Arrival_time','Duration','Price','Fare_Route_Description'],keep='first')
    df_data['search_and_departure_time_match'] = np.where(df_data['Time_searched_against']==df_data['Departure_time'],'match','no match')


    df_data.to_csv(fp+fn, index=False)
    


def generateurl(downinfo,upinfo):
    """
    This generates a list of urls based on provided date,route, time,toc_type and searchtype information, which are then fed to the NRE website

    Parameters:
    downinfo:  a list of lists with data for down routes [[direction of travel,dateoftravel,[org stn, dest stn],[depart times],toc/all toc flags,fixed/relative search]
    upinfo: a list of lists with data for up routes [[direction of travel,dateoftravel,[org stn, dest stn],[depart times],toc/all toc flags,fixed/relative search]

    Returns:
    combinedupanddownurls: a list of lists containting information for both up and down routes
    """

    
    urldown = getrouteurl(downinfo)
    urlup = getrouteurl(upinfo)

    #combine both up and down routes into a new common list
    combinedupanddownurls = urldown + urlup

    return combinedupanddownurls
        
  
def getdatetimesinfo(routesandtimes, dateoffset):
    """
    This is an 'initialisation' procedure which sets most of the parameters for the functioning of the whole process.
    It takes a date and derives the dates for the future based on metadata provided 
    and then derives the appropriate days, origin and destination routes and departure times for each of these factors
    
    Parameters:
    routesandtimes: A dataframe holding routes and times information
    dateoffset:     An integer representing the number of days to alter the date of search by.  DEFAULT is 0 days

    Returns:
    datesandtimes:  A default dictionary containing {dateoftravel+startstationcode:[[up journey],[times],[down journey],[times],[toc_filter],[search_type]]}

    """
      
    #increment date to check if needed
    datetocheck = datetime.today()+timedelta(days=dateoffset)
    
    #initialisation information
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    
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
        
        daystomoveahead = routesandtimes[count][8]

        searchtype = routesandtimes[count][9]

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

            downdatesandtimes.append(["downroute",formattedfuturedate,downroute,downtimestocheck,toc_filter,searchtype])
            updatesandtimes.append(["uproute",formattedfuturedate, uproute,uptimestocheck,toc_filter,searchtype])
    
    return downdatesandtimes,updatesandtimes


def gettingquerydata(fp):
    """
    This reads in route,times,toc_filter and search type information from an excel file. It also converts this excel data into a list of lists to be plugged into
    the function gettimesdatesinfo.

    Parameters:
    fp: a string containing the filepath of the data file holding route and time info

    Returns:
    a list of list with [[uproutes,downroutes],[downweekdays],[downsaturday],[downsunday],[upweekdays],[upsaturdays],[upsundays],[toc_filter],[search_type and search_date]]
    """
    
    raw_data = pd.read_excel(fp)

    del raw_data['variable name']

    todaysdate = datetime.today()
    
    final_list = []
    temp_list = []
    
    for count, items in enumerate(raw_data):
        
        routesup = raw_data.iloc[2,count].split(',') 
        routesdown = raw_data.iloc[3,count].split(',')
    
        routes = [routesup, routesdown]
        temp_list.append(routes)

        downweekdaytime = raw_data.iloc[4,count].split(',')
        temp_list.append(downweekdaytime)
    
        downsaturdaytime = raw_data.iloc[5,count].split(',')
        temp_list.append(downsaturdaytime)

        downsundaytime = raw_data.iloc[6,count].split(',')
        temp_list.append(downsundaytime)

        upweekdaytime = raw_data.iloc[7,count].split(',')
        temp_list.append(upweekdaytime)

        upsaturdaytime = raw_data.iloc[8,count].split(',')
        temp_list.append(upsaturdaytime)

        upsundaytime = raw_data.iloc[9,count].split(',')
        temp_list.append(upsundaytime)

        toc_filter = raw_data.iloc[0,count]
        temp_list.append(toc_filter)

        #handle search criteria here
        searchfilter = raw_data.iloc[1,count]
        searchterms = getdaysahead(searchfilter)
        temp_list.append(searchterms)

        if len(searchterms) == 1:
            futuredate = todaysdate+timedelta(days=searchterms[0])
            searchtype = f"Fixed to the future date, {futuredate.strftime('%d/%m/%Y')}"
        else:
            searchtype = f"Relative to today, {todaysdate.strftime('%d/%m/%Y')}"
        
        temp_list.append(searchtype)
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


def getdaysahead(searchstring):
    """
    This handles the information from search type held in the metadata.  If it's a relative search, splits the comma-separated values in the string into a list of values for the days to move ahead.
    If it's a fixed date, it derives the number of days from today to the desired search date and passes that on as a list

    Parameters:
    searchstring:   A string containing the search type specified in the metadata

    Returns:
    dayslist:       A list containing the days ahead to generate results for.

    """
    if 'days ahead' in searchstring:
        #split filter by day, split into list of number strings and then convert into a list of ints
        days = searchstring.split("days",1) # split string by 'days'
        dayslist = days[0].split(",") #split numbers into a list of string chars
        dayslist = [int(i) for i in dayslist] # convert into a list of ints
        return dayslist
        
    if "departing on" in searchstring:
        # extract date from the last 10 characters of the searchstring and convert to a datetime format
        search_date = datetime.strptime(str(searchstring[-10:]),'%d/%m/%Y')
        
        #calculate the number of days between current date and fixed date of travel
        daysahead = (search_date - datetime.today()).days

        dayslist = [daysahead]
        
        #handle if datediff is negative
        if dayslist[0] < 0:
            print("fixed date is now in the past")
            dayslist = [100]
        else:

            return dayslist
            
    else:
        print(searchstring)
        print("Your search criteria is wrong.")
        dayslist = [100]    
        return dayslist

        
def getrouteurl(route):
    """
    This function takes a list of lists representing direction/route/times/dates information and parses this information into a URL which will be sent to the NRE 
    website later.  There is a nested if structure to reflect the choices as to type of search carried out 1) ALL TOCS and Relative Date, 2) ANY TOC and Relative 
    Date, 3) All TOCS and Fixed, 4), Any TOC and Fixed

    Parameters:
    route:  A list of lists with route information, from generateurl

    Returns:
    urllist: A list holding the parsed URLs ready to sent the the NRE server

    """
    
    urllist = list()

    for trip in route:
            #  CASE: ALL TOCs and Relative search
            if  "All TOCs" in trip[4] and 'Relative' in trip[5]:
      
                for tcounter,times in enumerate(trip[3],0):
                
                    url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly'  


                    if "//dep" in url:
                        print(f"No times supplied for time {trip[3]} and {url}")
                    else:
                        
                        urllist.append([trip[4],url,trip[3][tcounter],trip[5]])
                        print(url)

            #CASE: Any TOC with a Relative search    
            elif 'Relative' in trip[5]:
                for tcounter,times in enumerate(trip[3],0):
                    url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+trip[1]+'/'+str(trip[3][tcounter])+'/dep/?directonly&show='+trip[4]                    
                #check if times have been supplied from the metadata
                    

                    if "//dep" in url:
                        print(f"No times supplied for time {trip[3]} and {url}")
                    else:
                        
                        urllist.append([trip[4],url,trip[3][tcounter],trip[5]])
                        print(url)
        
            #CASE:  All TOCs with a Fixed Search
            elif "All TOCs" in trip[4] and 'Fixed' in trip[5]:
                for tcounter,times in enumerate(trip[3],0):
                
                    fixed_date = trip[5][-10:].replace("/20","/").replace("/","")
                    url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+fixed_date+'/'+str(trip[3][tcounter])+'/dep/?directonly'                    
                #check if times have been supplied from the metadata
                    
                
                    if "//dep" in url:
                        print(f"No times supplied for time {trip[3]} and {url}")
                    else:
                        
                        urllist.append([trip[4],url,trip[3][tcounter],trip[5]])
                        print(url)

            #CASE Any TOC with a Fixed search          
            elif 'Fixed' in trip[5]:
                for tcounter,times in enumerate(trip[3],0):
                    fixed_date = trip[5][-10:].replace("/20","/").replace("/","")
                    url = 'https://ojp.nationalrail.co.uk/service/timesandfares/'+trip[2][0]+'/'+trip[2][1]+'/'+fixed_date+'/'+str(trip[3][tcounter])+'/dep/?directonly&show='+trip[4]                    
                #check if times have been supplied from the metadata

                    if "//dep" in url:
                        print(f"UP INFO: No times supplied for time {trip[3]} and {url}")
                    else:
                        
                        urllist.append([trip[4],url,trip[3][tcounter],trip[5]])
                        print(url)
    return urllist



#routine boilerplate
if __name__ == '__main__':
    main()