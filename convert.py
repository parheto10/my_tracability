import sys
import os
from geojson import Feature, Point, FeatureCollection, Polygon
import json
#import geojson
from pprint import pprint

#print(sys.version)

path=r'd:\temp\test.json'
regions  = os.path.join('ci.json')

with open(regions,'r') as data_file:
    data = json.load(data_file)
    #print(data)
    for lat, lng in data:
        print(lat, lng)

feature_collection = FeatureCollection(data['features'])


# def show_map(request):  
#     #creation of map comes here + business logic
#     m = folium.Map([51.5, -0.25], zoom_start=10)
#     test = folium.Html('<b>Hello world</b>', script=True)
#     popup = folium.Popup(test, max_width=2650)
#     folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
# 
#     context = {'my_map': m}
# 
#     return render(request, 'polls/show_folium_map.html', context)

