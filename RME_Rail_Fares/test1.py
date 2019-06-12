from datetime import datetime, timedelta
import calendar 

def main():
    for i in range(0,0):  
        print(i)

    print("hello")
    
    print("date")
    olddate = datetime.today()
    olddatename = calendar.day_name[olddate.weekday()]

    print("\ndate with offset")
    newdate = datetime.today()+timedelta(days=2)
    
    newdatename = calendar.day_name[newdate.weekday()]

    if olddatename == "Wednesday":
        print ("today is today")
    else:
        print("unexpected")

    if newdatename == "Friday":
        print("today is funday")


if __name__ == '__main__':
    main()

