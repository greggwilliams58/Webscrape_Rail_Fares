import urllib.request
import json
import pprint as pp


def main():

    #resp = getlocation("high")
    #print(resp)
    #
    #for place in resp:
    #    print( f"The location {place['label']} has the code {place['code']}")

    resp = getfares("cov","cdf")
    #print(type(resp))
    pp.pprint(resp)
    #pp.pprint(resp['dest']['code'])
    #pp.pprint(resp['fares'][2]['adult'])

    pp.pprint(resp.get('dest','no dest').get('code','no code'))
    pp.pprint(resp.get('orig', 'no orig').get('code','no orig code'))

    for counter, items in enumerate(resp,0):
        #pp.pprint(resp)
        pp.pprint(resp.get('fares','no dest')[counter].get('adult','no code').get('fare','no fares'))
        pp.pprint(resp.get('fares','no dest')[counter].get('ticket','no ticket').get('name','no name'))
        pp.pprint(resp.get('fares', 'no fares')[counter].get('fare_setter','no setter').get('name','no name'))
    
    #for k,v in resp.items():
        #print(f"{k} has value {v}")
        #print(resp.get('fares','no fares found').get('category','no cat'))
        #print(v['orig'])




def getlocation(loc):
    response = urllib.request.urlopen(f"http://api.brfares.com/ac_loc?term={loc}").read().decode("utf-8")
    jcontents = json.loads(response)

    return jcontents


def getfares(loc1,loc2):
    response = urllib.request.urlopen(f"http://api.brfares.com/querysimple?orig={loc1}&dest={loc2}").read().decode("utf-8")

    jcontents = json.loads(response)

    return jcontents

if __name__ == '__main__':
    main()