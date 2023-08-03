import folium
import pandas as pd
from IPython.display import display, IFrame
# create map centered around California
map_california = folium.Map(location=[36.7783, -119.4179], zoom_start=6)  
df = pd.read_csv("map.csv", sep=',')
print(df.head())
# add markers for each university
for _, row in df.iterrows():
    folium.Marker(location=[row[0], row[1]], 
                  popup=row[2], 
                  icon=folium.Icon(color='blue')).add_to(map_california)

# Save the map to an HTML file
map_california.save('map.html')

# Display the map using IFrame
IFrame(src='map.html', width=800, height=500)