import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
from collections import defaultdict
import csv


def main():
    formatted_date = datetime.now().strftime('%Y%m%d_%H-%M')

    filepath = 'C:\\Users\\gwilliams\\Desktop\\Python Experiments\\work projects\\RME_Rail_Fares\\'
    filename = f'RME_data_{formatted_date}.csv'

    collecteddata = collatedata()


    #test URLS
    #urlstoprocess =  {'140519':'http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/140519/1430/dep','150519':'http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/150519/1430/dep'}

    # the real process here
    #full list of URLs to be generated
    urlstoprocess = generateurl(collecteddata)
    
    print("getting NRE data now...")
    rawjsondata=[]
    for counter, items in enumerate(urlstoprocess,1):
        print(f"getting item {counter} of {len(urlstoprocess)}")

        response = urllib.request.urlopen(items[1])
        soup = BeautifulSoup(response,'html.parser')

        td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text

        jsonData = json.loads(td_class)
        jsonData['jsonJourneyBreakdown'].update(TravelDate = items[0])
        
        rawjsondata.append(jsonData)

    processjson(rawjsondata,filepath,filename)



def processjson(jsoninfo,fp, fn):
    
    print("preparing the csv file")
    #create a blank csv object
    datafile = open(fp + fn, 'w',newline='')
    csvwriter = csv.writer(datafile)


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

    csvwriter.writerow(response_header)

    response = []
    for journey in jsoninfo:
        response.append(datetime.now().strftime('%Y%m%d_%H-%M'))
        traveldate = journey['jsonJourneyBreakdown']['TravelDate'].zfill(6)
        traveldate = traveldate[0:1] + '/' + traveldate[2:4] + '/' + traveldate [5:6] 
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

        csvwriter.writerow(response)

        response = []

    datafile.close()

    





def generateurl(collecteddata):
    urltoprocess = {}
    tempurldown = []
    tempurlup = []


    dateoftravel = list(collecteddata.keys())

    for date in dateoftravel:
        
        for data in collecteddata[date]:
            if data[0][0] ==  'KGX':
                for counter,downtime in enumerate(data[1],0):
                    url = [date,'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[0][0]+'/'+data[0][1]+'/'+date+'/'+str(data[1][counter])+'/dep/']
                    tempurldown.append(url)

                    
            if data[2][0] == 'EDB':
                for counter,updtime in enumerate(data[3],0):
                    url = [date,'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[2][0]+'/'+data[2][1]+'/'+date+'/'+str(data[3][counter])+'/dep/']
                    tempurlup.append(url)


    urltoprocess = tempurldown + tempurlup
    #pp.pprint(urltoprocess)

    return urltoprocess
        

   
def collatedata(basedate = datetime.today()):
  

    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

    datesandtimes = defaultdict(list)
    
    originanddestination = [['KGX','EDB'],['EDB','KGX']]

    downweekdaytimes = ['0612','0900','1000','1030','1200','1300','1330','1500','1530','1400','1900']
    downsaturdaytimes = ['0612','0830','0900','0930','1130','1200','1230','1430','1500','1530','1800']
    downsundaytimes = ['0848','0900','0930','1030','1100','1122','1230','1300','1330','1530','1600','1630','1900']

    upweekdaytimes = ['0656','0830','0900','1030','1130','1400','1430','1530','1731','1830','1936']
    upsaturdaytimes = ['0626','0655','0930','1000','1130','1200','1330','1400','1630','1700']
    upsundaytimes = ['1030','1100','1430','1450','1630','1700','1800','1830']

    datetocheck = datetime.today()+timedelta(days=1)
   
    daystomoveahead = [1,7,30]
    datestocheck = []

    for counter,item in enumerate(daystomoveahead):
        futuredate = basedate + timedelta(daystomoveahead[counter])

        formattedfuturedate, dayofweek = futuredate.strftime('%d%m%y'), weekdays[futuredate.weekday()]
        #print(f"This is the day ahead {formattedfuturedate},  {dayofweek} ")

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

        datesandtimes[formattedfuturedate] = [[originanddestination[0],downtimestocheck,originanddestination[1],uptimestocheck]]

    return datesandtimes



if __name__ == '__main__':
    main()



