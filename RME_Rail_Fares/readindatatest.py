import pandas as pd

def main():
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


    print(final_list[0][1])


if __name__ == '__main__':
    main()



