import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
from collections import defaultdict

def main():

    todaydate = setdates()

    
    #response = urllib.request.urlopen(f"http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/200419/1830/dep/")
    #soup = BeautifulSoup(response,'html.parser')

    ##datapackage = list()

    ##print(soup)

    ##with open("Full text from NRE.txt","w") as f:
    ##    f.write(soup.text)

    ##for i in range (1,6):
    #td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text
        
    #jsonData = json.loads(td_class)
    #print(jsonData)
    
      
    
    ##print(datapackage[0]['jsonJourneyBreakdown']['arrivalStationName'])  
    ##print(datapackage[0]['jsonJourneyBreakdown']['departureStationName'])
    
    ##for counter,items in enumerate(datapackage):
    #   ##pp.pprint(F"This is counter {counter}")
    #   ##pp.pprint(f"This is items {items}")
    #   ##print(type(counter))
    #   ##print(type(items))


    ##    pp.pprint(items.get('singleJsonFareBreakdowns','no')[0])
    ##    pp.pprint(resp.get('fares','no dest')[counter].get('adult','no code').get('fare','no fares'))
    ##    print(items['singleJsonFareBreakdowns'][counter]['nreFareCategory'])
    ##    print(items['singleJsonFareBreakdowns'][counter]['fullFarePrice'])
   
def setdates():

    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    weekdaytimes = ['0612','0900','1000','1200','1300','1400','1500','1900']
    saturdaytimes = ['0612','0830','0900','1130','1200','1430','1500','1800']
    sundaytimes = ['0848','0900','1130','1200','1430','1500','1800']
    datesandtimes = defaultdict(list)
    

    todaysdate = datetime.today()

    daystomoveahead = [1,7,30]
    datestocheck = []

    for counter,item in enumerate(daystomoveahead):
        futuredate = todaysdate + timedelta(daystomoveahead[counter])
        print(futuredate)
        formattedfuturedate, dayofweek = futuredate.strftime('%d%m%y'), weekdays[futuredate.weekday()]
        #print(f"This is the day ahead {formattedfuturedate},  {dayofweek} ")

        daycheck = weekdays[futuredate.weekday()]
        if daycheck in ("Monday","Tuesday","Wednesday","Thursday","Friday"):
            daytocheck = 'weekday'
            timestocheck = weekdaytimes
        elif daycheck in ("Saturday"):
            daytocheck = 'saturday'
            timestocheck = saturdaytimes
        elif daycheck in ("Sunday"):
            daytocheck = 'sunday'
            timestocheck = sundaytimes
        else:
            print("error")

        datesandtimes[formattedfuturedate] = timestocheck
        

    for date,times in datesandtimes.items():
        print(date)
        print(times)
    

    #datestosearch = [dayaheaddate,weekaheaddate,monthaheaddate]
    #print(type(datestosearch))
    #return datestosearch




if __name__ == '__main__':
    main()