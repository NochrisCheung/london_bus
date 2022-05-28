import requests
from requests.auth import HTTPBasicAuth
import json

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
        except Exception as e:
            print(f"Error querying lines for {mode}")
            return

        return [results['lineId'], results['lineName'], results['direction'], results['mode'], results['orderedLineRoutes'][0]['name'],results['orderedLineRoutes'][0]['naptanIds']]

    def get_route(self, line_id, direction):
        # Request and return station ids
        self.request_count += 1

        try:
            request_url = f"https://api.tfl.gov.uk/Line/{line_id}/Route/Sequence/{direction}"
            r = requests.get(request_url, auth=self.auth, headers=self.headers)
            results = r.json()

            all_bus_lines = []
            for line in results:
                all_bus_lines.append([line['id'], line['name'], line['modeName'], line['mode'], line['created'], line['modified'], line['routeSections']])

        except Exception as e:
            print(f"Error querying route for {line_id}")
            return

        return all_bus_lines

APIKEY = "a328020e810c4e19b9952b6485351e2e"

tfl_api = TflAPI(APIKEY)
bus_route = tfl_api.get_route(1, "inbound")
all_bus_lines = tfl_api.get_all_bus_line()

id = 1
direction = "inbound"
# [?serviceTypes][&excludeCrowding]
bus_route = requests.get("https://api.tfl.gov.uk/Line/Mode/bus/Route")
parsed = json.loads(bus_route.content)

for key, value in parsed[0].items():
    print(key, value)
parsed[0].keys()
parsed['orderedLineRoutes']
parsed["stations"][0]
parsed["orderedLineRoutes"]
for key, value in parsed["stations"][0].items():
    print(key)


for stations in parsed['stopPointSequences'][0]['stopPoint']:
    print(stations["name"])
for key, value in parsed.items():
    print(key)

parsed['stopPointSequences'][0].keys()

parsed['stopPointSequences'][0]['stopPoint'][0]['name']




print(json.dumps(parsed, indent=4))





func parse_json(json_file):
    parsed = json.loads(json_file.content)


bus_sequence = requests.get("https://api.tfl.gov.uk/Line/1/StopPoints")
bus_routes = requests.get("https://api.tfl.gov.uk/Line/1/Route")
br_parsed = json.loads(bus_routes.content)
print(json.dumps(br_parsed, indent=4, sort_keys=True))

for key, value in parsed[1].items():
    print(key, value)

parsed[0].keys()
print(json.dumps(parsed, indent=4, sort_keys=True))
