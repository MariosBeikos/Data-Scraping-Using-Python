#import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
#from matplotlib import cm
from PIL import Image
import os

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

# Read every 8 line (8 lines in .marios file is data for one city)
for i in range(int(len(TxtList)/8)):
    a.append([])
    for j in range(8*i,8*i+8):
        a[i].append(TxtList[j].split(","))


# Main data list
DataList=[]
for i in range(int(len(TxtList)/8)):
    DataList.append( [  a[i][0] , a[i][1] , [a[i][2],a[i][3],a[i][4],a[i][5],a[i][6],a[i][7]]  ] ) # All the elements 

# Check the list
#print(DataList)

DataTxt.close()
# Finish reading the file





# Ge tthe coordinates and the links (the links will be used to extract the names ofe the cities)
Links = []
Coords = []
for i in range(len(DataList)):
    Links.append(DataList[i][0][0])
    Coords.append( (round(float(DataList[i][1][1]),4) , round(float(DataList[i][1][0]),4) ) )  # Coords = (φ,λ) (lat,lon) # round bcz the library reads only numbers with a precision of 4??

# Get the names of the file
Names = []
for i in Links:
    a = i.find("en/gr/") + len("en/gr/")
    b = i.find("/",a)
    Names.append( i[a:b].capitalize() ) # name is between a & b

#print(Names)
#print(Coords)

# Create a list with sets of the data we are going to use to make the maps 
Points = []
for i in range(len(DataList)):
    Points.append( { "name": Names[i] ,"coords": Coords[i] } ) 

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

# Main Function; to create a map (later to put in a "for" loop) ### OLD - UNUSED
def MakeMapOld(List,DateStr,NameStr,UnitStr):


    variable = List

    # Create a map
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())  # Use the PlateCarree projection

    # Set the map extent to focus on Greece
    ax.set_extent([20, 30, 34, 42], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot points and label the variable
    for j, point in enumerate(Points):
        lon, lat = point["coords"]
        ax.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.PlateCarree())
        ax.text(
            lon + 0.2, lat,  # Adjust the label position slightly to avoid overlap
            f"{point['name']} ({variable[j]}"+UnitStr+")", 
            transform=ccrs.PlateCarree(),
            fontsize=10,
            color='blue'
        )

    # Add a title
    plt.title(NameStr+" "+DateStr, fontsize=16)

    # Show the map
    ##plt.show()

    # Save the image in a folder named "Images" that has the same path as this .py file
    plt.savefig("./Images/" + str(i) + ".png", dpi=300)






def MakeMap(List,DateStr,NameStr,UnitStr):


    variable = List

    # Create a map
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())  # Use the PlateCarree projection

    # Set the map extent to focus on Greece
    ax.set_extent([19, 30, 34, 42], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot points and label the variable
    for j, point in enumerate(Points):
        lon, lat = point["coords"]
        ax.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.PlateCarree())
        ax.text(
            lon + 0.2, lat,  # Adjust the label position slightly to avoid overlap
            f"{point['name']} ({variable[j]}"+UnitStr+")", 
            transform=ccrs.PlateCarree(),
            fontsize=10,
            color='blue'
        )

    # Add a title
    plt.title(NameStr+" "+DateStr, fontsize=16)


     # Add a scalebar (with a length of 5 km)
    length_km = 5  # Length of the scalebar in kilometers
    map_proj = ccrs.PlateCarree()
    scalebar = AnchoredSizeBar(ax.transData, length_km, f'{ int(round(length_km*(458/5))) } km', loc='lower left', pad=0.1,
                               borderpad=0.5, sep=5, size_vertical=0.05, color='black', frameon=False)
    ax.add_artist(scalebar)    
    
    
    
    # Add a north arrow (pointing towards the top of the map)
    ax.annotate(
        'N', xy=(0.9, 0.95), xycoords='axes fraction',
        xytext=(0.9, 0.85), textcoords='axes fraction',
        arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', lw=5),
        fontsize=25, color='black', ha='center', va='center'
    )

    # Add gridlines
    ax.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.4)



    # Show the map
    ##plt.show()

    # Save the image in a folder named "Images" that has the same path as this .py file
    plt.savefig("./Images/" + str(i) + ".png", dpi=300)












# variable to label on the map (e.g., temperature in °C, precip)
Variables = []
for i in range(len(DataList)):  ####|### Last input here:
    Variables.append(DataList[i][2][4]) # precipitation ######################## # Option (last input): 2 = Max Temp; 3 = Low Temp; 4 = Precip; ##########################################

# Create a list with the data for every city: basically, previous data was n*m now its m*n
VarInTime = []  # Variable in time
for i in range(len(Variables[0])):
    a = []
    for j in range(len(Coords)):
        a.append(Variables[j][i])
    VarInTime.append(a)


DataList[0][2][0] # Days (['Tonight', 'Sun', 'Mon', )
DataList[0][2][1] # Dates (['Tonight', '1/12', '1/13']) the format is american: "Month/Day"
# Switch the Date format from "Month/Day" to "Day/Month" in the main data list
for i in range(len(DataList[0][2][0])):
    Month = DataList[0][2][1][i].split("/")[0]
    Day = DataList[0][2][1][i].split("/")[1]
    DataList[0][2][1][i] = Day+"/"+Month


# Append the corrected-format dates to a new list
DatesList = []
for i in range(len(DataList[0][2][0])):
    DatesList.append(DataList[0][2][0][i]+" " + DataList[0][2][1][i] )


#print(DatesList)

# Call the function
# Option: 2 = Max Temp; 3 = Low Temp; 4 = Precip; 
#MakeMap(Variables[0],DatesList[0],"WeatherData","%") # ° °

# Call the main function to create n (10) number of images
for i in range(len(VarInTime)):
    pass
    #print(VarInTime[i]);print(DatesList[i])
    MakeMap(VarInTime[i],DatesList[i],"Precipitation:","%")  # ° ° ############################################### Call the Function ###############################

# Number of images
NOfImages = len(VarInTime)
for i in range(NOfImages):
    pass
    #print(i)

'''
# Create GIF
Images = []
for i in range(NOfImages):
    a = open("./Images/"+str(i)+".png","r")
    Images.append(a)

print(type(Images[0]))


Images[0].save(
    "output_animation.gif",
    save_all=True,
    append_images=Images[1:],  # Add remaining frames
    duration=1000,             # Duration of each frame (milliseconds)
    loop=0                    # 0 for infinite loop
)
'''


# Create animated .gif file

# Folder containing the images
image_folder = "Images"
output_gif = "Output.gif"

# Get a sorted list of all image files
image_files = sorted(
    [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]
)

# Open all images using PIL and store them in a list
frames = [Image.open(img) for img in image_files]

# Save the first image and append the rest to create a GIF
frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],  # Add remaining frames
    duration=1000,             # Frame duration in milliseconds
    loop=0,                    # Infinite loop
)



print("-------------------------END-------------------------")