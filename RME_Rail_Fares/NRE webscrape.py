import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
from collections import defaultdict



def main():

    collecteddata = collatedata()

    #print(collecteddata)
    #test URLS
    #urlstoprocess =  {'140519':'http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/140519/1430/dep','150519':'http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/150519/1430/dep'}

    # the real process here
    #full list of URLs to be generated
    urlstoprocess = generateurl(collecteddata)
    print(type(urlstoprocess))

    for k,v in urlstoprocess.values():
        pp.pprint( f":{k} {v}")
#        for times in v:
#            pp.pprint(times)

    print("getting url info")

    rawjsondata = list()
    
    
    #for k,v in urlstoprocess.items():

    #    response = urllib.request.urlopen(v)
    #    soup = BeautifulSoup(response,'html.parser')

    #    td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text

   #     jsonData = json.loads(td_class)
   #     jsonData['jsonJourneyBreakdown'].update(TravelDate = k)

   #     rawjsondata.append(jsonData)

   # answer = processjson(rawjsondata)



def processjson(jsoninfo):
    for journey in jsoninfo:
        print(type(journey))
        print (f"travel date \t {journey['jsonJourneyBreakdown']['TravelDate']}")
        print (f"arrival \t {journey['jsonJourneyBreakdown']['arrivalStationName']}")
        print(f"departure \t{journey['jsonJourneyBreakdown']['departureStationName']}")
        print(f"time \t{journey['jsonJourneyBreakdown']['departureTime']}")
        print(f"type \t{journey['singleJsonFareBreakdowns'][0]['breakdownType']}")
        print(f"1st class \t{journey['singleJsonFareBreakdowns'][0]['cheapestFirstClassFare']}")
        print(f"discount \t{journey['singleJsonFareBreakdowns'][0]['discount']}")
        print(f"fareprovider \t{journey['singleJsonFareBreakdowns'][0]['fareProvider']}")
        print(f"route \t{journey['singleJsonFareBreakdowns'][0]['fareRouteDescription']}")
        print(f"route name\t{journey['singleJsonFareBreakdowns'][0]['fareRouteName']}")
        print(f"ticket type\t fullfare{journey['singleJsonFareBreakdowns'][0]['fareTicketType']}")
        print(f"full fare \t{journey['singleJsonFareBreakdowns'][0]['fullFarePrice']}")
        print(f"nre category \t{journey['singleJsonFareBreakdowns'][0]['nreFareCategory']}")
        print(f"ticket price \t{journey['singleJsonFareBreakdowns'][0]['ticketPrice']}")





def generateurl(collecteddata):
    urltoprocess = defaultdict(list)
    tempurldown = list()
    tempurlup = list()

    dateoftravel = list(collecteddata.keys())

    for date in dateoftravel:
        #print(date)
        for data in collecteddata[date]:
            if data[0][0] ==  'KGX':
                for counter,downtime in enumerate(data[1],0):
                    url = 'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[0][0]+'/'+data[0][1]+'/'+date+'/'+str(data[1][counter])+'/dep/'
                    
                    
                    
                
            if data[2][0] == 'EDB':
                for counter,updtime in enumerate(data[3],0):
                    url = 'http://ojp.nationalrail.co.uk/service/timesandfares/'+data[2][0]+'/'+data[2][1]+'/'+date+'/'+str(data[3][counter])+'/dep/'
                    tempurlup.append(url)
    urltoprocess[date] = [tempurldown,tempurlup]               
    print(date)
    
    #pp.pprint(tempurldown)
    #pp.pprint(tempurlup)
    #urltoprocess[date] = [tempurldown,tempurlup]
    
    #for k,v in urltoprocess.items():
    #    print(k)
    #    print(v)

    return urltoprocess
        

   
def collatedata(basedate = datetime.today()+timedelta(days=2)):
  

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



