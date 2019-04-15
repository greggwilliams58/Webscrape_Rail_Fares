import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp
from datetime import datetime, timedelta



def main():

    todaydate = setdates()

    
    response = urllib.request.urlopen(f"http://ojp.nationalrail.co.uk/service/timesandfares/KGX/EDB/200419/1830/dep/220419/1200/dep")
    soup = BeautifulSoup(response,'html.parser')

    #datapackage = list()

    ##print(soup)

    #with open("Full text from NRE.txt","w") as f:
    #    f.write(soup.text)

    #for i in range (1,6):
    #    td_class = soup.find('script',{ 'id':f'jsonJourney-4-{i}' }).text
        
    #    jsonData = json.loads(td_class)
    #    datapackage.append(jsonData)
    
    #for item in datapackage:
    #    pp.pprint(item)
    #    print("new record \n")
        
    
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
    todaysdate = datetime.today()
    #dayahead = datetime.today() + timedelta(todaysdate=1)
    #weekahead = todaysdate + timedelta(days=7)
    #monthahead = todaysdate +timedelta(month=1)


    currentdate = dayahead.strftime('%d%m%y')
    print(f"This is the day ahead {currentdate}")


    


    return currentdate



if __name__ == '__main__':
    main()