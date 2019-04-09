import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp




def main():

    response = urllib.request.urlopen(f"http://ojp.nationalrail.co.uk/service/timesandfares/PAD/RDG/today/1900/dep")
    soup = BeautifulSoup(response,'html.parser')

    datapackage = list()

    for i in range (1,6):
        td_class = soup.find('script',{ 'id':f'jsonJourney-4-{i}' }).text
        
        jsonData = json.loads(td_class)
        datapackage.append(jsonData)
        pp.pprint(jsonData)
        
    
    print(datapackage[0]['jsonJourneyBreakdown']['arrivalStationName'])  
    print(datapackage[0]['jsonJourneyBreakdown']['departureStationName'])
    
    for counter,items in enumerate(datapackage):
       #pp.pprint(F"This is counter {counter}")
       #pp.pprint(f"This is items {items}")
       #print(type(counter))
       #print(type(items))


       pp.pprint(items.get('singleJsonFareBreakdowns','no')[0])
       # pp.pprint(resp.get('fares','no dest')[counter].get('adult','no code').get('fare','no fares'))
    #    print(items['singleJsonFareBreakdowns'][counter]['nreFareCategory'])
    #    print(items['singleJsonFareBreakdowns'][counter]['fullFarePrice'])
    



if __name__ == '__main__':
    main()