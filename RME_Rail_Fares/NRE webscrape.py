import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
from collections import defaultdict
import csv
import pandas as pd


def main():
    formatted_date = datetime.now().strftime('%Y%m%d_%H-%M')

    #file paths to be used in the office
    #routesandtimedatafp = 'C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Faresdatafile.xlsx'
    #filepath = 'C:\\Users\\gwilliams\\Desktop\\Python Experiments\\work projects\\RME_Rail_Fares'


    #file paths to be used when working at home
    routesandtimedatafp = 'C:\\Users\\gregg_000\\Documents\\GitHub\\RME_Rail_Fares\\datafile.xlsx'
    filepath = 'C:\\Users\\gregg_000\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares\\'
    filename = f'RME_data_{formatted_date}.csv'

    alltimesdates = gettingquerydata(routesandtimedatafp)
    #pp.pprint(alltimesdates)
    
    #generated the sets of dates and times to work with
    collateddatesandtime = getdatetimesinfo(alltimesdates)

    #pp.pprint(collateddatesandtime)
    #full list of URLs to be generated
    urlstoprocess = generateurl(collateddatesandtime)
    
    print("getting NRE data now...")

    #extracting the data from the webset and converting to json
    jsondata = extractwebdata(urlstoprocess)

    #convert the json into csv format and save externally
    processjson(jsondata,filepath,filename)


def extractwebdata(urlstr):
    """
    This makes a call to the NRE webset and parses the html, selecting the relevant journey data as json format
    it also adds the travel date to the json dataset

    Parameters 
    urlstr:         A list of urls to be used to interrogate the NRE website

    Returns:
    rawjsondata     A list of json-formatted journey information 
    """

    rawjsondata=[]
    for counter, items in enumerate(urlstr,1):
        print(f"getting item {counter} of {len(urlstr)}")

        response = urllib.request.urlopen(items[1])
        soup = BeautifulSoup(response,'html.parser')

        #extract the required json data
        td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text

        #convert the json data into a dictionary
        jsonData = json.loads(td_class)

        #add the travel date information to the json data
        jsonData['jsonJourneyBreakdown'].update(TravelDate = items[0])
        
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

    #create a blank csv object
    datafile = open(fp + fn, 'w',newline='')
    
    #create a csvwriter object
    csvwriter = csv.writer(datafile)

    #create a header for the csv file
    response_header = []
    
    response_header.append('date_data_generated')
    response_header.append('travel_Date')
    response_header.append('departure_station')
    response_header.append('arrival_station')
    response_header.append('departure_time')
    response_header.append('breakdown_time')
    response_header.append('cheapest_first_class')
    response_header.append('discount')
    response_header.append('fare_provider')
    response_header.append('route_description')
    response_header.append('route_name')
    response_header.append('ticket_type')
    response_header.append('full_price')
    response_header.append('nre_fare_category')
    response_header.append('ticketprice')

    #write the csv header row
    csvwriter.writerow(response_header)

    #extract data from the json file
    response = []
    for journey in jsoninfo:
        #derived formatted date for date of data extraction
        response.append(datetime.now().strftime('%Y%m%d_%H-%M'))
        
        #fill travel date trailing zeros
        traveldate = str(journey['jsonJourneyBreakdown']['TravelDate']).zfill(6)
        #add / marks to avoid excel formatting doing odd things
        traveldate = traveldate[0:2] + '/' + traveldate[2:4] + '/' + traveldate [4:6]
        #add the formatted travel date to list
        response.append(traveldate)
        response.append(journey['jsonJourneyBreakdown']['departureStationName'])
        response.append(journey['jsonJourneyBreakdown']['arrivalStationName'])
        response.append(journey['jsonJourneyBreakdown']['departureTime'])
        response.append(journey['singleJsonFareBreakdowns'][0]['breakdownType'])
        response.append(journey['singleJsonFareBreakdowns'][0]['cheapestFirstClassFare'])
        response.append(journey['singleJsonFareBreakdowns'][0]['discount'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareProvider'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareRouteDescription'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareRouteName'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fareTicketType'])
        response.append(journey['singleJsonFareBreakdowns'][0]['fullFarePrice'])
        response.append(journey['singleJsonFareBreakdowns'][0]['nreFareCategory'])
        response.append(journey['singleJsonFareBreakdowns'][0]['ticketPrice'])

        #write data to the row of the csv file
        csvwriter.writerow(response)

        #flush the list to prepare for the next row
        response = []

    #close the file and export the data
    datafile.close()

    
def generateurl(collecteddateinfo):
    """
    This generates a list of urls based on provided date,route and time information, which are then fed to the NRE website

    Parameters:
    collecteddateinfo:  a default dictionary {dateoftravel:[[up journey],[times],[down journey],[times]]}

    Returns:
    urltoprocess:       a list containting travel date and url information [traveldate, url]
    """

    urltoprocess = {}
    tempurldown = []
    tempurlup = []

    #extract dates of travel from keys of dictionary
    routesoftravel = list(collecteddateinfo.keys())
    #pp.pprint(routesoftravel)
    #walk through dates, routes and times to create url
    #pp.pprint(dateoftravel)


    for routeanddate in routesoftravel:
        #pp.pprint(routeanddate)
        for counter,data in enumerate(collecteddateinfo[routeanddate]):

            if routeanddate[6:] ==  data[1][0]:
                #print(f"this is down route extract {routeanddate[6:]}({routeanddate}) and this is the data extract {data[1][0]}")
                for counter,downtime in enumerate(data[2],0):
                    #print(counter)
                    url = [data[0],'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[1][0]+'/'+data[1][1]+'/'+data[0]+'/'+str(data[2][counter])+'/dep/']
                    print(url)
                    tempurldown.append(url)

                    
            if routeanddate[6:] == data[1][1]:
                #print(f"this is up route extract {routeanddate[3:6]} and this is the data extract {data[1][1]}")
                for counter,uptime in enumerate(data[3],0):
                    url = [data[0],'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[3][0]+'/'+data[3][1]+'/'+data[0]+'/'+str(data[4][counter])+'/dep/']
                    print(url)
                    tempurlup.append(url)

    #combine both up and down routes into a new common list
    urltoprocess = tempurldown + tempurlup
    
    return urltoprocess
        
  
def getdatetimesinfo(routesandtimes, dateoffset = 0):
    """
    This is an 'initialisation' procedure which sets most of the parameters for the functioning of the whole process
    It takes a date and derives the dates 1,7 and 30 days in the future and then dertives the appropriate days, origin and destination routes and departure times for each of these factors
    
    Parameters:
    dateoffset:     An integer representing the number of days to alter the date of search by.  DEFAULT is 0 days

    Returns:
    datesandtimes:  A default dictionary containing {dateoftravel:[[up journey],[times],[down journey],[times]]}

    """
    #pp.pprint(routesandtimes)
    
    #increment date to check if needed
    datetocheck = datetime.today()+timedelta(days=dateoffset)
    
    #initialisation information
    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    
    daystomoveahead = [1,7,30]
    #populate defaultdict with values depending on date increments day of the week
    
    datesandtimes = defaultdict(list)
    
    ###start loop with all the dates and times here
    for count, items in enumerate(routesandtimes):
        originanddestination = routesandtimes[count][0]
      
        downweekdaytimes = routesandtimes[count][1]
        downsaturdaytimes = routesandtimes[count][2]
        downsundaytimes = routesandtimes[count][3]

        upweekdaytimes = routesandtimes[count][4]
        upsaturdaytimes = routesandtimes[count][5]
        upsundaytimes = routesandtimes[count][6]
        
        startpoint = routesandtimes[count][0][0][0]
        endpoint = routesandtimes[count][0][0][1]

        for upanddown in routesandtimes[count][0]:
            #print(f"this is upanddown[0] {upanddown[0]}")
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

                datesandtimes[ formattedfuturedate + upanddown[0]] = [[formattedfuturedate,   originanddestination[0],downtimestocheck,originanddestination[1],uptimestocheck]]
    
            
    pp.pprint(datesandtimes)
    return datesandtimes


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
        
        routesup = raw_data.iloc[0,count].split(',') 
        routesdown = raw_data.iloc[1,count].split(',')
    
        routes = [routesup, routesdown]
        temp_list.append(routes)

        downweekdaytime = raw_data.iloc[2,count].split(',')
        temp_list.append(downweekdaytime)
        
        downsaturdaytime = raw_data.iloc[3,count].split(',')
        temp_list.append(downsaturdaytime)

        downsundaytime = raw_data.iloc[4,count].split(',')
        temp_list.append(downsundaytime)

        upweekdaytime = raw_data.iloc[5,count].split(',')
        temp_list.append(upweekdaytime)

        upsaturdaytime = raw_data.iloc[6,count].split(',')
        temp_list.append(upsaturdaytime)

        upsundaytime = raw_data.iloc[7,count].split(',')
        temp_list.append(upsundaytime)

        final_list.append(temp_list)

        temp_list = []

    return final_list




if __name__ == '__main__':
    main()