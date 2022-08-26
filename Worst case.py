# data based on : https://openflights.org/data.html
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point,LineString

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

ax.scatter([flights['start_lon'],flights['end_lon']],[flights['start_lat'],flights['end_lat']])

plt.show()
