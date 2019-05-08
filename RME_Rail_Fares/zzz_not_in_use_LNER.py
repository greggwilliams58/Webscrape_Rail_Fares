import urllib.request
from bs4 import BeautifulSoup
import json
import pprint as pp


def main():

    response = urllib.request.urlopen(f"https://www.lner.co.uk/buy-tickets/booking-engine/?od=London+Kings+Cross&onlc=6121&ocrs=KGX&dd=Edinburgh&dnlc=9328&dcrs=EDB&DepartureDate=10+April%2C+2019&outy=2019&outd=10&outm=04&outda=y&DepartureTime=15%3A00&outh=15&outmi=00&ret=y&isOpenReturn=false&ReturnDate=10+April%2C+2019&rety=2019&retd=10&retm=04&retda=y&ReturnTime=19%3A00&reth=19&retmi=00&nad=1&nch=0&totalPassengers=1&totalPassengersMinimum=1&hasRailCards=false&RailCardCode=&RailCardQuantity=1&rc=&rcn=&TravelViaFlag=false&TravelAvoidFlag=false&v=&vnlc=&vcrs=&nv=&nvnlc=&nvcrs=&tto=0&pc=&cc=&tsc=0&Clearpromo=0&refC=&inToc=&firstClassTicketsOnly=False&orderId=&brandName=")
    soup = BeautifulSoup(response,'html.parser')

    datapackage = list()
    print(type(soup))
    print(soup)

if __name__ == '__main__':
    main()