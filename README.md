# Webscrape_Rail_Fares
Application for getting data from NRE Website for the RME Team.
Version 3.1
Written by Greg Williams at ORR, 21st February 2020

## WHAT'S NEW
Bug fixed: up and down routes are both returned by the same column of metadata, rather than just down routes

## HOW TO INSTALL
If application has been recieved as a zip file, it should be unzipped to a location of your choice.

## HOW TO USE
go to the //dist/RME_webscrape folder to review instructions.  Once the excel sheet has been filled with search parameters, use the .exe file to extract data from the NRE website.

## FOLDER LOCATIONS AND THEIR MEANINGS
The first three folders in this location are relevant.  All other folders and files (apart from the one ending in .exe) should be ignored

### 1_READ_ME_Instructions
This folder contains a copy of these instructions

### 2_Routes_and_times_metadata
This folder contains an excel spreadsheet which hold metadata which defines the type of TOCs to be searched for, the kind of dates to be searched for, the routes and the times to be searched for

### 3_Data_goes_here
This folder contains temporary daily dataloads, which are deleted at the end of each execution

### 3_Data_goes_here\\appended_data
This is where the completed datasets are appended to previous datasets.  There should be three kinds of appended file
A) All_appended_data: Both Fixed and Relative Search types
B) fixed appended data: Just the appended search types
C) relative appended data: Just the relatiive search types 


## USE OF METADATA
Edit this Excel file to specify the TOCs, search types. routes and times you want to search against
The first column is fixed
All other columns may be edited.

Column 1: Variable Name - This is fixed and are descriptions of each of the variables.
Column 2 and others are lists of routes and times, which can be edited.

### Variable Descriptions:
TOC Filter: This specified if the search in this column (routes/times) for "All TOCs" or just one TOC
Project Type: This defines whether the dates searched for are a given number of day(s) away from the date the code is executed, OR the date searched for is a given day in the future.
origin and destination down: routes which run away from London
origin and destination up: routes which run up towards London

downweekdaytimes: times for searching on down routes, Monday-Friday
downsaturdaytimes: times for searching on down routes, Saturday
downsundaytimes: times for searching on down routes, Sunday

upweekdaytimes: times for searching on up routes, Monday-Friday
upsaturdaytimes: times for searching on up routes, Saturday
upsundaytimes: times for searching on up routes, Sunday


## FORMATTING OF DATA.
This is important as if metadata is in the incorrect format then then application will fail to run.
FORMATTING OF TOC Filter
This item cannot be left blank
If you want no filter, use "All TOCs"
If you want a TOC filter, use the appropriate TOC code.  This can be found via the NRE website, run a search and look for the last two letter at the end of the URL from the returned answer.
(eg show=GW  for GWR from the string https://ojp.nationalrail.co.uk/service/timesandfares/PAD/BRI/today/1145/dep?show=GW)

## FORMATTING OF PROJECT TYPE:
1) Relative to execution date: "'n1,n2,n3,n days ahead from today"  (The leading apstrophe is to force a text data type. the list of comma-separated numbers with no spaces is followed by the phrase "days ahead from today")
2) Fixed to future date: "'departing on DD/MM/YYYY" (The leading apstrophe is to force a text data type.  The phrase "departing on " is followed by a date in the format DD/MM/YYYY.  The date should always be in the future.

## FORMATTING OF ROUTES
Stations are given in the three letter CRS code, which can be found by running a dummy query for your route on the NRE website (https://www.nationalrail.co.uk/default.aspx)
A comma is used as the separator between origin and destination stations.
Down routes have non-london station first, london station second; up routes are reversed.

## FORMATTING OF TIMES:
All times should be in text format, with an Apostrophe at the front to enforce text format.
Times are in HHMM format, with a comma as the separator.
If no times are required, a single comma should be in the cell.  This is required for the running of the application and to serve as an "intentionally blank" placeholder.
