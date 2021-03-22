# import folium
# from django.http import request
# # from django.shortcuts import get_object_or_404
# # from django.contrib.auth.models import User
# # from cooperatives.models import Cooperative, Parcelle
# #
# # cooperative = get_object_or_404(Cooperative, pk=id)
# # parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id)
#
# #import pandas
# map = folium.Map(location=[5.349390, -4.017050], zoom_start=5)
# # for parcelle in parcelles:
# #     map = folium.Map(location=[5.349390, -4.017050], zoom_start=5)
# #     lat = parcelle.latitude
# #     long = parcelle.longitude
# #     fg = folium.Marker(lat, long)
# # # fg.add_to(folium.GeoJson(data=(open('ci.json', 'r', encoding='utf-8').read())))
# #     map.add_to(fg)
# map.save('carte3.html')
#
# '''
# map = folium.Map(location=[5.349390, -4.017050], zoom_start=5)
# folium.Marker([folium.GeoJson(data=(open('ci.json', 'r', encoding='utf-8-sig').read()))]).add_to(map)
#
# map.save("carte2.html")
#
#
# map = folium.Map(location=[5.349390, -4.017050], zoom_start=5)
# regions = folium.GeoJson(data=(open('ci.json', 'r', encoding='utf-8-sig').read())).add_to(map)
# points = folium.Marker([regions.lat, regions.long]).add_to(map)
# #for lon, lat in points:
# #folium.Marker([points.lat, points.lon]).add_to(map)
# map.save("carte2.html")
# '''
# """ import folium
# import os
# map = folium.Map(location=[5.349390, -4.017050], zoom_start=8)
# regions  = os.path.join('ci.json')
#
# folium.GeoJson((regions), name="Cote D'Ivoire").add_to(map) """
#
# #map.save("map1.html")
#