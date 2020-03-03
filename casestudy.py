'''
#Author: TRAPTI DAMODAR BALGI
#Emp Id: 142907
#Version 1.0
'''

import pandas as pd
import matplotlib.pyplot as plt
import osmapi
import gmplot
#import os

# CO emission

DF = pd.read_csv('City Drive 2.csv')
AREA = []
TIME = []
T1 = []

EMISSION = list(DF.iloc[:, 27])
TIME = DF['Trip Time(Since journey start)(s)']

R = len(EMISSION)

for i in range(0, R-1):
    if EMISSION[i] == '-':
        EMISSION[i] = '0'
    if float(EMISSION[i]) > 205.0:
        AREA.append(EMISSION[i])
        T1.append(TIME[i])

print(AREA)

plt.scatter(T1, AREA, color="r")
plt.xlabel("Time")
plt.ylabel("Polluted Area")
plt.title("CO emission")
plt.legend()
plt.show()


# Speed Zones

SPEED_VIOLATION = []
LEVEL = []
LONGI = []
LATI = []
SPEED = []

DF = pd.read_csv("City Drive 2.csv")
LONGITUDE = DF[" Longitude"]
LATITUDE = DF[" Latitude"]
LEVEL1 = DF[" G(z)"]
SPEED = DF["Speed (GPS)(km/h)"]
GPSTIME = DF["GPS Time"]

for i in DF.index:
    if SPEED[i] > 50:
        SPEED_VIOLATION.append([DF[' Latitude'][i], DF[' Longitude'][i]])
        LONGI.append(LONGITUDE[i])
        LATI.append(LATITUDE[i])
for j in DF.index:
    if LEVEL1[j] > 17:
        LEVEL.append([DF[' Latitude'][j], DF[' Longitude'][j]])
        LONGI.append(LONGITUDE[j])
        LATI.append(LATITUDE[j])

GMAP1 = gmplot.GoogleMapPlotter(17.46, 78.377, 13)

plt.scatter(LONGI, LATI, label='level', color='k')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Speed Violation')
plt.legend()
plt.show()

# plotting the coordinates on google map
GMAP1.scatter(LATI, LONGI, '# FF0000', size=50, maker=False)
GMAP1.plot(LATI, LONGI, 'cornflowerblue', edge_width=5)
GMAP1.draw(r"Libraries\Documents\map1.html")

# plotting the coordinates on open street map
API = osmapi.OsmApi(API="https://api06.dev.openstreetmap.org",
                    username=u"chsuryapradeepsp@gmail.com",
                    password=u"surya@123")
API.ChangesetCreate({u"comment": u"Speed Violation"})

for i in range(len(SPEED_VIOLATION)):
    print(API.NodeCreate({u"lon": SPEED_VIOLATION[i][1],
                          u"lat": SPEED_VIOLATION[i][0], u"tag": {}}))
for j in range(len(LEVEL)):
    print(API.NodeCreate({u"lon": LEVEL[j][1],
                          u"lat": LEVEL[j][0], u"tag": {}}))

# Analysis of fuel

DF = pd.read_csv("City Drive 2.csv")
DIST = DF['Trip Distance(km)']
FUEL = DF['Fuel Remaining (Calculated from vehicle profile)(%)']

FINAL = DIST.iloc[-1]
FINAL = float(FINAL)
print("The total distance covered:", FINAL)

REM_FUEL = FUEL.iloc[-1]
REM_FUEL = float(REM_FUEL)

USED = 100 - REM_FUEL
USED = USED / 100
print("fuel used for the trip:", USED)

KMPL = DF["Kilometers Per Litre(Instant)(kpl)"].replace(to_replace='-', value='0')

for i in range(len(KMPL)):
    KMPL[i] = float(KMPL[i])

X = KMPL.mean()
print("kpml avg:", X)
X = X * USED
print("exp distance", X)
DIFF = X - FINAL
print("The deviation between actual and expected distance with the fuel:", DIFF)

# Detection of potholes

DF = pd.read_csv("City Drive 2.csv")

def find_potholes(accln, DF):
    '''
    function to find potholes
    '''
    potholes = []
    length = len(accln)
    #TIME_RANGE = range(0, length)
    for i in range(1, length - 1):
        if isinstance(accln[i], float) and isinstance(accln[i - 1], float)\
        and isinstance(accln[i + 1], float):
            if accln[i] < accln[i - 1] and accln[i] < accln[i + 1]:
                potholes.append([DF[' Latitude'][i],
                                 DF[' Longitude'][i],
                                 (accln[i + 1] - accln[i])])
    pothole = pd.DataFrame(data=potholes, columns=['Latitude', 'Longitude',
                                                   'Pothole_Gradient'])
    return pothole


ACCELZ = DF["Acceleration Sensor(Z axis)(g)"] \
         # reading acceleration sensor(z axis) into dataframe ACCELZ
SPEED = DF["GPS Speed (Meters/second)"]  # reading GPS Speed into dataframe SPEED
POTHOLE = find_potholes(ACCELZ, DF)
HIGHEST_THRESHOLD_POTHOLE = max(POTHOLE['Pothole_Gradient'])
LOWER_THRESHOLD_POTHOLE = (1 / 3) * max(POTHOLE['Pothole_Gradient'])
LOW_PRIORITY = []
HIGH_PRIORITY = []

for ind in POTHOLE.index:
    if POTHOLE['Pothole_Gradient'][ind] <= LOWER_THRESHOLD_POTHOLE:
        LOW_PRIORITY.append([POTHOLE['Latitude'][ind],
                             POTHOLE['Longitude'][ind],
                             POTHOLE['Pothole_Gradient'][ind]])
        break
else:
    HIGH_PRIORITY.append([POTHOLE['Latitude'][ind],
                          POTHOLE['Longitude'][ind],
                          POTHOLE['Pothole_Gradient'][ind]])
LOW_PRIORITY = pd.DataFrame(data=LOW_PRIORITY,
                            columns=['Latitude', 'Longitude', 'Intensity'])
HIGH_PRIORITY = pd.DataFrame(data=HIGH_PRIORITY,
                             columns=['Latitude', 'Longitude', 'Intensity'])

# plotting the latitude vs longitude
plt.scatter(LOW_PRIORITY['Latitude'], LOW_PRIORITY['Longitude'],
            label='low priority pothole')
plt.scatter(HIGH_PRIORITY['Latitude'], HIGH_PRIORITY['Longitude'],
            label='High priority pothole')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.legend()
plt.title('Pothole Analysis and plotting')
plt.show()

# plotting the coordinates on google map
GMAP1 = gmplot.GoogleMapPlotter(17.46, 78.377, 13)
GMAP1 = gmplot.GoogleMapPlotter(17.46, 78.377, 13)
GMAP1.heatmap(HIGH_PRIORITY['Latitude'], HIGH_PRIORITY['Longitude'])
GMAP1.draw("gmplot_map1.html")
GMAP2 = gmplot.GoogleMapPlotter(17.46, 78.377, 13)
GMAP2.heatmap(LOW_PRIORITY['Latitude'], LOW_PRIORITY['Longitude'])
GMAP2.draw("gmplot_map2.html")
