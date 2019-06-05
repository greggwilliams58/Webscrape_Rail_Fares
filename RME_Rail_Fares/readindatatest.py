import pandas as pd
import pprint as pp


def main():
    querydata = gettingquerydata()

    print(querydata[0][0][0][0]) # departure down 1
    print(querydata[0][0][0][1]) # departure up 1
    print(querydata[0][0]) # down route 1
    print(querydata[0][1]) #  down weekday 1
    print(querydata[0][2]) # down saturday 1
    print(querydata[0][3]) # down sunday 1
    print(querydata[0][4]) # up weekday 1
    print(querydata[0][5]) # up saturday 1
    print(querydata[0][6]) # up sunday 1



    print(querydata[1][0][0][0]) # departure down 2
    print(querydata[1][0][0][1]) # departuren up 2
    print(querydata[1][0]) # down route 2
    print(querydata[1][1]) #  down weekday 2
    print(querydata[1][2]) # down saturday 2
    print(querydata[1][3]) # up sunday 2
    print(querydata[1][4]) # up weekday 2
    print(querydata[1][5]) # up saturday 2
    print(querydata[1][6]) # up sunday 2



def gettingquerydata():
    raw_data = pd.read_excel('C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\datafile.xlsx')
    
    print(raw_data)
    del raw_data['variable name']

    #print(raw_data)

    final_list = []
    temp_list = []
    
    for count, items in enumerate(raw_data):
        print(count)
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

    #pp.pprint(final_list)
    



    return final_list


if __name__ == '__main__':
    main()



