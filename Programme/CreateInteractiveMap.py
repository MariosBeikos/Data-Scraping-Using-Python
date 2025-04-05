#import geopandas as gpd
#import matplotlib.pyplot as plt
import folium
#from PIL import Image
#import os

print("------------------------START------------------------")
# Read the .marios file

# Open the txt file in read mode
DataTxt = open("Data.marios","r")
# Get the length of the file by two ways and chek they are the same

# Initialize a variable-counter and an emnpty list
Counter = 0 
TxtList = []
for i in DataTxt:
    Counter +=1 
    TxtList.append(i)
FileLen = int((Counter - 2)/8)

# Print if second to last item is as expected
print(TxtList[-2] == "END\n")

# Get the data of the data (last row)
Date = TxtList[-1][13:]
#print(Date)

# Remove two last rows
TxtList = TxtList[:-2]

# Print true if length is as expected
print(FileLen == len(TxtList)/8)

# Strip every "\n" and all the list elements
for i in range(len(TxtList)):
    TxtList[i] = str(TxtList[i]).strip("\n")

# Create a temporaty list 
a = b = c = []

''' # Not used code
for i in range(int(len(TxtList)/8)):
    a.append(TxtList[i])
    for j in range(1,int(len(TxtList)/(len(TxtList)/8))):
        print(i,j)
        for k in range(0):
            print(i,j,k)
'''

for i in range(int(len(TxtList)/8)):
    a.append([])
    for j in range(8*i,8*i+8):
        a[i].append(TxtList[j].split(","))

# Main data list
DataList=[]
for i in range(int(len(TxtList)/8)):
    DataList.append( [  a[i][0] , a[i][1] , [a[i][2],a[i][3],a[i][4],a[i][5],a[i][6],a[i][7]]  ] )

# Check the list
#print(DataList)

DataTxt.close()
# Finish reading the file





# Get the names of the file
Links = []
Coords = []
for i in range(len(DataList)):
    Links.append(DataList[i][0][0])
    Coords.append( (round(float(DataList[i][1][1]),6) , round(float(DataList[i][1][0]),6) ) )  # Coords = (φ,λ) (lat,lon)

# Get the names of the cities from the links
Names = []
for i in Links:
    a = i.find("en/gr/") + len("en/gr/")
    b = i.find("/",a)
    Names.append( i[a:b].capitalize() ) # between position a & b stands the name if the city

#print(Names)
#print(Coords)



#print(Points)

'''
# variable to label on the map (e.g., temperature in °C, precip)
Variables = []
for i in range(len(DataList)):
    Variables.append(DataList[i][2][4]) # precipitation ########################


# Strip the ° from every string ############################################
for i in range(len(Variables)):
    for j in range(len(Variables[0])):
        Variables[i][j] = Variables[i][j].strip("°")

print(Variables)

VarInTime = []  # Variable in time
for i in range(len(Variables[0])):
    a = []
    for j in range(len(Coords)):
        a.append(Variables[j][i])
    VarInTime.append(a)
'''




# variable to label on the map popup (high temp)
Variables = []
for i in range(len(DataList)):  
    Variables.append(DataList[i][2][2]) # high temperature, option 2 


VarInTime2 = []  # Variable in time
for i in range(len(Variables[0])):
    a = []
    for j in range(len(Coords)):
        a.append(Variables[j][i])
    VarInTime2.append(a)


# variable to label on the map popup (low temp)
Variables = []
for i in range(len(DataList)): 
    Variables.append(DataList[i][2][3]) # low temperature, option 3

VarInTime3 = []  # Variable in time
for i in range(len(Variables[0])):
    a = []
    for j in range(len(Coords)):
        a.append(Variables[j][i])
    VarInTime3.append(a)



# variable to label on the map popup (precip)
Variables = []
for i in range(len(DataList)): 
    Variables.append(DataList[i][2][4]) # precipitation, option 4

VarInTime4 = []  # Variable in time
for i in range(len(Variables[0])):
    a = []
    for j in range(len(Coords)):
        a.append(Variables[j][i])
    VarInTime4.append(a)


# all variables in one list
VarInTime = [VarInTime2,VarInTime3,VarInTime4]








DataList[0][2][0] # Days List (['Tonight', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon'])
DataList[0][2][1] # DatesList (['1/11', '1/12', '1/13', '1/14', '1/15', '1/16', '1/17', '1/18', '1/19', '1/20'])
# Change teh Date format form "month/day" (american), to "day/month" (normal)
for i in range(len(DataList[0][2][0])):
    Month = DataList[0][2][1][i].split("/")[0]
    Day = DataList[0][2][1][i].split("/")[1]
    DataList[0][2][1][i] = Day+"/"+Month

# Appends them to a seperate list
DatesList = []
for i in range(len(DataList[0][2][0])):
    DatesList.append(DataList[0][2][0][i]+" " + DataList[0][2][1][i] )

#print(DatesList)


n: int = 1 ############################################################################################################################ choose forecast day n=0: tonight n=9: 9 days after (max n=9, integer!)

#print(VarInTime,"\n",DatesList,"\n",Names,"\n",Coords)

# Create points with {sets} of attributes: lat, lon, name, date ...
Points = []
for i in range(len(DataList)):
    #print(i)
    Points.append( { "lat": Coords[i][1] , "lon": Coords[i][0], "name": Names[i], "date": DatesList[n], "highTemp": VarInTime[0][n][i], "lowTemp": VarInTime[1][n][i], "precip": VarInTime[2][n][i], "comment": DataList[i][2][5][n] } ) 



# Create a base map centered at Greece
map = folium.Map(location=[38.5000, 23.5000], zoom_start=7,max_bounds=True,control_scale=True)
# Set the bounds for the map
#map.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])
#map.fit_bounds([[25,15], [50,35]])
# Add a callback to prevent zooming/panning outside the bounds
map.options['maxBoundsViscosity'] = 0.4  # Prevent zooming and panning outside bounds


# Add markers to the map
for point in Points:
    folium.CircleMarker(
        location=[point["lat"], point["lon"]],
        radius=7,
        color="red",
        fill=True,
        fill_color="yellow",
        fill_opacity=0.6, 
        tooltip=folium.Tooltip(f"{point['name']}"),
        #tooltip=f"City: {point['name']}",
        #popup=f"City: {point['name']}\nDate:{point['date']}",
        popup=folium.Popup(f"City: {point['name']}<br>Date: {point['date']}<br>High: {point['highTemp']}C<br>Low: { point['lowTemp']}C<br>Precipitation: {point['precip']}%<br>Comments: {point['comment']}", max_width=300),
    ).add_to(map)

# Save the map to an HTML file
map.save("InteractiveMap.html")

# Add Layer
#folium.LayerControl().add_to(map)



print("-------------------------END-------------------------")

