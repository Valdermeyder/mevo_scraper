import folium
from folium.plugins import MarkerCluster
import csv
from bike_service_proxy import BikeServiceProxy

bikes_map = folium.Map(location=[54.34632, 18.649246])
bikes_cluster = MarkerCluster()
bikes_proxy = BikeServiceProxy()


def get_battery_info(battery_level):
    if battery_level is None:
        return 'Unknown'
    return f'{battery_level}%'


def get_bike_color(battery_level):
    if battery_level is None:
        return 'gray'
    elif battery_level > 50:
        return 'green'
    elif battery_level > 20:
        return 'orange'
    return 'red'


bikes_file = bikes_proxy.current_locations_file
bikes_reader = csv.DictReader(bikes_file)
for station_row in bikes_reader:
    available_bikes = int(station_row['DOSTĘPNE ROWERY'])
    if available_bikes > 0:
        available_bike_ids = station_row['NUMERY DOSTĘPNYCH ROWERÓW'].split(',')
        location = list(map(float, station_row['WSPÓŁRZĘDNE'].split(', ')))
        for bike_id in available_bike_ids:
            battery_level = bikes_proxy.battery_info_for_bike(bike_id)
            battery_info = get_battery_info(battery_level)
            bike_info = f'ID: {bike_id}\nBattery: {battery_info}'
            bike_color = get_bike_color(battery_level)
            bike_icon = folium.Icon(icon='bicycle', prefix='fa', color=bike_color)
            bikes_cluster.add_child(folium.Marker(location, popup=bike_info, icon=bike_icon))

bikes_map.add_child(bikes_cluster)
bikes_map.save('../demo/index.html')
