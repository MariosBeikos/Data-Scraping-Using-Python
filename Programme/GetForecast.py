# PagesSeperately
print("------------------------START------------------------")

from selenium import webdriver
from bs4 import BeautifulSoup
import re 
import time

#####Set the Timer for the freeze:
Timer = 5 # seconds
####Set the desired links for the cities and their corresponding coordinates 
Links = ["https://www.accuweather.com/en/gr/athens/182536/weather-forecast/182536","https://www.accuweather.com/en/gr/volos/185462/weather-forecast/185462","https://www.accuweather.com/en/gr/heraklion/2282907/weather-forecast/2282907"]
Coords = [ [37.983286434153314,23.726906539828743], [39.36658059424113,22.95120199675449], [35.338152063452405,25.14210013028715]] # CRS: WGS 84' , ESPG = 4326

# Ge the local time of running this code
TimeOfSearch = time.localtime()
# Each element of the above is the: Year/Month/Day/Hour/Min/Sec.... get the ones you want
Date  =  ( str(TimeOfSearch[2]) +"/"+ str(TimeOfSearch[1])+"/"+str(TimeOfSearch[0]) )
#check
#print("Day of data: " + Date)

Soups = []

for link in Links:
    # Set up Selenium with a Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
 
    # Open the page
    driver.get(link)
    time.sleep(Timer)  # Wait for the page to load, especially if there's JavaScript rendering
    

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    Response = soup.prettify()
    # print(Response)

    # Clean up
    driver.quit()
    Soups.append(soup)


# Ge the local time of running this code
TimeOfSearch = time.localtime()
# Each element of the above is the: Year/Month/Day/Hour/Min/Sec.... get the ones you want
DataDate  =  ( str(TimeOfSearch[2]) +"/"+ str(TimeOfSearch[1])+"/"+str(TimeOfSearch[0]) )
#check
print("Day of data: " + DataDate)




#def GetData(Soup):  ; AthanesData = GetData(Soups[0])

# Find from the box all the names of the days in chronological order
DayName = soup.find_all('p', class_='day')
# Initiate a an empty  list to fill later
DayNameList = []

# Iterate for every day to get its name
for i in range(len(DayName)):
    # Find the beggining of the designated element 
    a1 = str(DayName[i]).find('<p class="day">') + len('<p class="day">')
    # Find the end of the designated element
    a2 = str(DayName[i]).find('</p>')
    # Get the in-between text
    a3 = str(DayName[i])[a1:a2]
    # Append it to the corresponding list
    DayNameList.append(a3)

#print(DayNameList)



# Find from the box all the names of the days in chronological order
Date = soup.find_all('div', class_='date')
# Initiate a an empty  list to fill later
DateList = []

# Iterate for every day to get its value
for i in range(len(Date)):
    # Find the beggining of the designated element 
    a1 = str(Date[i]).find('<p>') + len('<p>')
    # Get a substring of the main string to exclude elements
    a2 = str(Date[i])[a1:a1+8]     
    # Find the end of the designated element
    a3 = a2.find('</p>')
    # Get the in-between text
    a4 = a2[0:a3]
    # Append it to the corresponding list
    DateList.append(a4)

#print(DateList)




# Find from the box all the Hight Temperatures chronological order
TempHi = soup.find_all('span', class_='temp-hi')
# Initiate a an empty  list to fill later
TempHiList = []

# Iterate for every day to get its value
for i in range(len(TempHi)):
    # Find the beggining of the designated element 
    a1 = str(TempHi[i]).find('<span class="temp-hi">') + len('<span class="temp-hi">')
    # Find the end of the designated element
    a2 = str(TempHi[i]).find('</span>')
    # Get the in-between text
    a3 = str(TempHi[i])[a1:a2]
    # Append it to the corresponding list
    TempHiList.append(a3)

#print(TempHiList)




# Find from the box all the Low Temperatures chronological order
TempLo = soup.find_all('span', class_='temp-lo')
# Initiate a an empty  list to fill later
TempLoList = []

# Iterate for every day to get its value
for i in range(len(TempLo)):
    # Find the beggining of the designated element 
    a1 = str(TempLo[i]).find('<span class="temp-lo">') + len('<span class="temp-lo">')
    # Find the end of the designated element
    a2 = str(TempLo[i]).find('</span>')
    # Get the in-between text
    a3 = str(TempLo[i])[a1:a2]
    # Append it to the corresponding list
    TempLoList.append(a3)

#print(TempLoList)




# find from the box all the Precipitation Data in chronological order
Precip = soup.find_all('div', class_='precip')
# Initiate a an empty  list to fill later
PrecipList = []

# Iterate for every day to get its value
for i in range(len(Precip)):
    # Find the beggining of the designated element 
    a1 = str(Precip[i]).find('</svg>') + len('</svg>')
    # Find the end of the designated element
    a2 = str(Precip[i]).find('</div>')
    # Get the in-between text
    a3 = str(Precip[i])[a1:a2]
    # Strip the unwanted values (\t & \n)
    a3 = a3.strip("\n").strip("\t").strip("\n").strip("\t").strip("\n").strip()
    # Convert to integer???
    a3 = int(a3.strip("%"))
    # Append it to the corresponding list
    PrecipList.append(a3)

#print(PrecipList)



# find from the box all the Precipitation Data in chronological order
Comms = soup.find_all('p', class_='no-wrap')
# Initiate a an empty  list to fill later
CommsListUnfiltered = []


# Iterate for every day to get its value
for i in range(len(Comms)):
    # Find the beggining of the designated element 
    a1 = str(Comms[i]).find('<p class="no-wrap">') + len('<p class="no-wrap">')
    # Find the end of the designated element
    a2 = str(Comms[i]).find('</p>')
    # Get the in-between text
    a3 = str(Comms[i])[a1:a2]
    # Append it to the corresponding list
    CommsListUnfiltered.append(a3)


# Initiate a an empty  list to fill with filtered values
CommsList = [] 
CommsList.append(CommsListUnfiltered[0])
# Filter values (remove 3rd, 5th, 7th, 9th ... etc.)
for i in range(1,len(CommsListUnfiltered),2):
    CommsList.append(CommsListUnfiltered[i])
    
#print((CommsList))

# Merge all lists into one 
DataList = [ DayNameList , DateList , TempHiList , TempLoList , PrecipList , CommsList ]
# Check Results 
for i in DataList:
    pass
    print(i)

# Feedback
print("def ran succeesfully!")



def GetData(x):
    soup = x 

    # Find from the box all the names of the days in chronological order
    DayName = soup.find_all('p', class_='day')
    # Initiate a an empty  list to fill later
    DayNameList = []

    # Iterate for every day to get its name
    for i in range(len(DayName)):
        # Find the beggining of the designated element 
        a1 = str(DayName[i]).find('<p class="day">') + len('<p class="day">')
        # Find the end of the designated element
        a2 = str(DayName[i]).find('</p>')
        # Get the in-between text
        a3 = str(DayName[i])[a1:a2]
        # Append it to the corresponding list
        DayNameList.append(a3)

    #print(DayNameList)



    # Find from the box all the names of the days in chronological order
    Date = soup.find_all('div', class_='date')
    # Initiate a an empty  list to fill later
    DateList = []

    # Iterate for every day to get its value
    for i in range(len(Date)):
        # Find the beggining of the designated element 
        a1 = str(Date[i]).find('<p>') + len('<p>')
        # Get a substring of the main string to exclude elements
        a2 = str(Date[i])[a1:a1+8]     
        # Find the end of the designated element
        a3 = a2.find('</p>')
        # Get the in-between text
        a4 = a2[0:a3]
        # Append it to the corresponding list
        DateList.append(a4)

    #print(DateList)




    # Find from the box all the Hight Temperatures chronological order
    TempHi = soup.find_all('span', class_='temp-hi')
    # Initiate a an empty  list to fill later
    TempHiList = []

    # Iterate for every day to get its value
    for i in range(len(TempHi)):
        # Find the beggining of the designated element 
        a1 = str(TempHi[i]).find('<span class="temp-hi">') + len('<span class="temp-hi">')
        # Find the end of the designated element
        a2 = str(TempHi[i]).find('</span>')
        # Get the in-between text
        a3 = str(TempHi[i])[a1:a2]
        # Append it to the corresponding list
        TempHiList.append(a3)

    #print(TempHiList)




    # Find from the box all the Low Temperatures chronological order
    TempLo = soup.find_all('span', class_='temp-lo')
    # Initiate a an empty  list to fill later
    TempLoList = []

    # Iterate for every day to get its value
    for i in range(len(TempLo)):
        # Find the beggining of the designated element 
        a1 = str(TempLo[i]).find('<span class="temp-lo">') + len('<span class="temp-lo">')
        # Find the end of the designated element
        a2 = str(TempLo[i]).find('</span>')
        # Get the in-between text
        a3 = str(TempLo[i])[a1:a2]
        # Append it to the corresponding list
        TempLoList.append(a3)

    #print(TempLoList)




    # find from the box all the Precipitation Data in chronological order
    Precip = soup.find_all('div', class_='precip')
    # Initiate a an empty  list to fill later
    PrecipList = []

    # Iterate for every day to get its value
    for i in range(len(Precip)):
        # Find the beggining of the designated element 
        a1 = str(Precip[i]).find('</svg>') + len('</svg>')
        # Find the end of the designated element
        a2 = str(Precip[i]).find('</div>')
        # Get the in-between text
        a3 = str(Precip[i])[a1:a2]
        # Strip the unwanted values (\t & \n)
        a3 = a3.strip("\n").strip("\t").strip("\n").strip("\t").strip("\n").strip()
        # Convert to integer???
        a3 = int(a3.strip("%"))
        # Append it to the corresponding list
        PrecipList.append(a3)

    #print(PrecipList)



    # find from the box all the Precipitation Data in chronological order
    Comms = soup.find_all('p', class_='no-wrap')
    # Initiate a an empty  list to fill later
    CommsListUnfiltered = []


    # Iterate for every day to get its value
    for i in range(len(Comms)):
        # Find the beggining of the designated element 
        a1 = str(Comms[i]).find('<p class="no-wrap">') + len('<p class="no-wrap">')
        # Find the end of the designated element
        a2 = str(Comms[i]).find('</p>')
        # Get the in-between text
        a3 = str(Comms[i])[a1:a2]
        # Append it to the corresponding list
        CommsListUnfiltered.append(a3)


    # Initiate a an empty  list to fill with filtered values
    CommsList = [] 
    CommsList.append(CommsListUnfiltered[0])
    # Filter values (remove 3rd, 5th, 7th, 9th ... etc.)
    for i in range(1,len(CommsListUnfiltered),2):
        CommsList.append(CommsListUnfiltered[i])
        
    #print((CommsList))

    # Merge all lists into one 
    DataList = [ DayNameList , DateList , TempHiList , TempLoList , PrecipList , CommsList ]
    # Check Results 
    for i in DataList:
        pass
        #print(i)  ####### Check

    # Feedback
    print("def ran succeesfully!")

    return DataList






AthensData = GetData(Soups[0])
VolosData = GetData(Soups[1])
HeraklionData = GetData(Soups[2])

CityData = [AthensData, VolosData, HeraklionData]

for i in CityData:
    pass
    #print(i)




#Coords ; Links ; ...Data

# Initialize the all-data-list
Data = []
# Append everything into one list
for i in range(len(Links)):
    Data.append( [  Links[i] , Coords[i] , CityData[i] ] )
    
print(Data)




# Create .txt-style file
DataTxt = open("Data.marios","w")

for i in Data:
    DataTxt.write(i[0])
    DataTxt.write("\n")
    DataTxt.write(str(i[1][0]));DataTxt.write(",");DataTxt.write(str(i[1][1]))
    DataTxt.write("\n")
    for j in i[2]:
        # Join the elements of each row with commas
        DataTxt.write(",".join(map(str, j)))
        DataTxt.write("\n")

#Idicator for data ending
DataTxt.write("END")
# Write an empty row
DataTxt.write("\n")
DataTxt.write("Day of data: " + DataDate)

# Close the file 
DataTxt.close()





print("-------------------------END-------------------------")