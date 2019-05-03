import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta
from collections import defaultdict



def main():

    todaydate = setdates()
    #print(todaydate)
    #pp.pprint(todaydate)
    #print(todaydate.values())
    

    #for date,times in todaydate.items():
    #   print(date ,times)
      

    originanddestination = [['KGX','EDB'],['EDB','KGX']]



    for routes in originanddestination:
        print(routes)
        for dayoftravel in todaydate.keys():
            for counter,_ in enumerate(dayoftravel,0):
                #for some reason this only prints 6 of each - 
                #I suspect the wrong object is being iterated over (dates rather than the list of times)
                if routes[0] ==  'KGX':
                    url = 'http://ojp.nationalrail.co.uk/service/timesandfares/'+routes[0]+'/'+routes[1]+'/'+dayoftravel+'/'+str(todaydate[dayoftravel][0][counter])+'/dep/'
                    print(url)

                elif routes[0] == 'EDB':
                    url = 'http://ojp.nationalrail.co.uk/service/timesandfares/'+routes[0]+'/'+routes[1]+'/'+dayoftravel+'/'+str(todaydate[dayoftravel][1][counter])+'/dep/'
                    print(url)


   
 
    #response = urllib.request.urlopen(f"http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/290519/1830/dep/")
    #soup = BeautifulSoup(response,'html.parser')

    ##datapackage = list()

    #print(soup)

    ##with open("Full text from NRE.txt","w") as f:
    ##    f.write(soup.text)

    #for i in range (1,6):
    #    td_class = soup.find('script',{ 'id':f'jsonJourney-4-1' }).text
    #    
    #jsonData = json.loads(td_class)
    #pp.pprint(jsonData)
    
      
    
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



   
def setdates(basedate = datetime.today()+timedelta(days=3)):
    

    weekdays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

    datesandtimes = defaultdict(list)
    
    
    downweekdaytimes = ['0612','0900','1000','1030','1200','1300','1330','1500','1530','1400','1900']
    downsaturdaytimes = ['0612','0830','0900','0930','1130','1200','1230','1430','1500','1530','1800']
    downsundaytimes = ['0848','0900','0930','1030','1100','1122','1230','1300','1330','1530','1600','1630','1900']

    upweekdaytimes = ['0656','0830','0900','1030','1130','1400','1430','1530','1731','1830','1936']
    upsaturdaytimes = ['0626','0655','0930','1000','1130','1200','1330','1400','1630','1700']
    upsundaytimes = ['1030','1100','1430','1450','1630','1700','1800','1830']

    #datetocheck = datetime.today()+timedelta(days=3)
   
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

        datesandtimes[formattedfuturedate] = [downtimestocheck,uptimestocheck]

    #print(type(datesandtimes))
    #pp.pprint(datesandtimes)



    return datesandtimes


#def settimes():
#    """
#    A collection of lists that define the departure times to be searched for
#    down = away from London
#    up = towards London
#    """
#
#    downweekdaytimes = ['0612','0900','1000','1030','1200','1300','1330','1400','1500','1530','1900']
#    downsaturdaytimes = ['0612','0830','0900','0930','1130','1200','1230','1430','1500','1530','1800']
#    downsundaytimes = ['0848','0900','0930','1030','1100','1122','1230','1300','1330','1530','1600','1630','1900']
#
#    upweekdaytimes = ['0656','0830','0900','1030','1130','1400','1430','1530','1731','1830','1936']
#    upsaturdaytimes = ['0626','0655','0930','1000','1130','1200','1330','1400','1630','1700']
#    upsundaytimes = ['1030','1100','1430','1450','1630','1700','1800','1830']#
#
#    return 


if __name__ == '__main__':
    main()



