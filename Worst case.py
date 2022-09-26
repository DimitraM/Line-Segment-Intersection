# data based on : https://openflights.org/data.html
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point,LineString
import numpy as np
import time

# get the start time
st = time.time()

flights =pd.read_csv(r'/home/dimitra/Documents/Domes/geopandas/2011_february_aa_flight_paths.csv')

# out of every line i make a new dataframe that has a collumn named 'geometry' which consists of LineStrings of 2 Poins each. Every Point has a Longitude and a Latitude. Fist Point simbolizes the
# departure and Second Point is for the landing
geometry = [LineString([[flights.iloc[i]['start_lon'], flights.iloc[i]['start_lat']], [flights.iloc[i]['end_lon'], flights.iloc[i]['end_lat']]]) for i in range(flights.shape[0])]
flights = gpd.GeoDataFrame(flights, geometry=geometry, crs='EPSG:4326')

fig = plt.figure(facecolor='#FCF6F5FF')
ax = plt.axes()

fig.set_size_inches(7, 3.5)
ax.patch.set_facecolor('#FCF6F5FF')

flights.plot(ax=ax, color='black', linewidth=0.1)

plt.setp(ax.spines.values(),color = 'black')
plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# The fligths are ready to be ploted
# plt.show()


#I make points out of longitude and latitude so i can see and where they intersect
flights['start_points'] = gpd.GeoDataFrame(gpd.points_from_xy(x=flights['start_lon'],y= flights['start_lat']))
flights['end_points'] = gpd.GeoDataFrame(gpd.points_from_xy(x=flights['end_lon'],y= flights['end_lat']))

# ax.scatter([flights['start_lon'],flights['end_lon']],[flights['start_lat'],flights['end_lat']])

# plt.show()

# class Points :
#     def __init__(self,x,y):
#         self.x = x
#         self.y = y
#
#     def display(self):
#         print("Latitude :", self.x)
#         print("Longitude :", self.y)


def onSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False

def orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0

def doIntersect(p1,q1,p2,q2):

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False


x= []
y= []
for index, row1 in flights.iterrows():
    for j, row2 in flights.iterrows():
        if doIntersect(row1['start_points'],row1['end_points'] , row2['start_points'], row2['end_points']) and row1['start_points']!=row2['start_points'] and row1['end_points']  != row2['end_points'] :
                print("Yes")
                res = row1['geometry'].intersection(row2['geometry'])
                x.append(res.x)
                y.append(res.y)
                # Add first scatter trace with medium sized markers
        else:
                print("No intersection")
                
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
ax.scatter(x,y)
plt.show()
