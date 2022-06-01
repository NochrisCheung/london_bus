import requests
from requests.auth import HTTPBasicAuth
import json
import time

APIKEY = "a328020e810c4e19b9952b6485351e2e"

class TflAPI:

    def __init__(self, app_key):
        self.app_key = app_key
        self.auth = HTTPBasicAuth('apikey', app_key)
        self.request_count = 0
        self.headers = {"Accept": "application/json"}

    def get_all_bus_line(self, travel_mode = "bus"):
    # Request and return all bus line names
        self.request_count += 1

        try:
            request_url = f"https://api.tfl.gov.uk/Line/Mode/{travel_mode}/Route"
            r = requests.get(request_url, auth=self.auth, headers=self.headers)
            results = r.json()

            all_bus_lines = []
            for line in results:
                all_bus_lines.append([line['id'], line['name'], line['modeName'], line['created'], line['modified'], line['routeSections']])

        except Exception as e:
            print(f"Error querying lines for {mode}")
            return

        return all_bus_lines

    def get_route(self, line_id, direction):
        # Request and return station ids
        self.request_count += 1

        try:
            request_url = f"https://api.tfl.gov.uk/Line/{line_id}/Route/Sequence/{direction}"
            r = requests.get(request_url, auth=self.auth, headers=self.headers)
            results = r.json()

        except Exception as e:
            print(f"Error querying route for {line_id}")
            return

        return [results['lineId'], results['lineName'], results['direction'], results['mode'], results['orderedLineRoutes'][0]['name'],results['orderedLineRoutes'][0]['naptanIds']]

    def get_station_gps_location(self, station_id):
        self.request_count += 1

        try:
            request_url = f"https://api.tfl.gov.uk/StopPoint/{station_id}"
            r = requests.get(request_url, auth=self.auth, headers=self.headers)
            results = r.json()

        except Exception as e:
            print(f"Error querying station gps location for {station_id}")
            return

        return [results['lat'], results['lon']]


# print(json.dumps(parsed, indent=4, sort_keys=True))
