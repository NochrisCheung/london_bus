import json
import pandas as pd
import tfl_api
import time

def save_json(file_name):
    # save file in json format
    data_loc = "/Users/nochris/Dropbox/My Mac (macbook-pro.lan)/Documents/london_bus_data"
    timestr = time.strftime("%Y-%m-%dT%H:%M:%S%Z")
    with open(f'{data_loc}/{file_name}_{timestr}.json', 'w') as f:
        json.dump(routes, f)

routes_df = pd.read_json('/Users/nochris/Dropbox/My Mac (macbook-pro.lan)/Documents/london_bus_data/bus_routes_2022-05-29T20:55:06BST.json')
routes_df.columns = routes_df.iloc[0]
routes_df = routes_df.rename(columns = routes_df.iloc[0]).iloc[1:]
routes_df

tfl_api = tfl_api.TflAPI(tfl_api.APIKEY)

# query all bus lines and save them as json
all_bus_lines = tfl_api.get_all_bus_line()
data_loc = "/Users/nochris/Dropbox/My Mac (macbook-pro.lan)/Documents/london_bus_data"
timestr = time.strftime("%Y-%m-%dT%H:%M:%S%Z")
with open(f'{data_loc}/all_bus_lines_{timestr}.json', 'w') as f:
    json.dump(all_bus_lines, f)

# query all stations of all bus lines and save them as json
routes = [['lineId','lineName','direction','mode','route_name','station_naptanIds']]
for bus_line in all_bus_lines:
    line_id = bus_line[0]
    print(bus_line[0])
    for dir in ['inbound', 'outbound']:
        time.sleep(1)
        try:
            routes.append(tfl_api.get_route(line_id, dir))
        except Exception as e:
            print("Error querying route")

data_loc = "/Users/nochris/Dropbox/My Mac (macbook-pro.lan)/Documents/london_bus_data"
timestr = time.strftime("%Y-%m-%dT%H:%M:%S%Z")
with open(f'{data_loc}/bus_routes_{timestr}.json', 'w') as f:
    json.dump(routes, f)


# query all bus stations gps locations and save as json
bus_route_df = pd.read_json('/Users/nochris/Dropbox/My Mac (macbook-pro.lan)/Documents/london_bus_data/bus_routes_2022-05-29T20:55:06BST.json')
bus_route_df = bus_route_df.rename(columns=bus_route_df.iloc[0])
bus_route_df = bus_route_df[1:]

all_stations = []
for stations in bus_route_df['station_naptan_ids']:
    all_stations = all_stations + stations

all_unique_stations = list(dict.fromkeys(all_stations))

station_id_to_gps_dict = {}
count = 0
for station in all_unique_stations:
    time.sleep(1)
    try:
        station_id_to_gps_dict[station] = tfl_api.get_station_gps_location(station)
        count = count + 1
        print(count, "-", station_id_to_gps_dict[station])
    except Exception as e:
        print("Error querying GPS locations for stations")
