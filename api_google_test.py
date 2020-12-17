import googlemaps
from datetime import datetime
import json
import pandas as pd

gmaps = googlemaps.Client(key = '')

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions(
    origin = "Calle Fuente Vaqueros, La Zubia, Granada",
    destination = "pizzeria verace, Granada",
    mode = "driving",
    departure_time = datetime.now()
)

with open("test3.json", "w") as f: json.dump(directions_result,f)

def preprocess_directions(directions_result):
    acc = []
    for step in directions_result[0]['legs'][0]['steps']:
        acc.append({
            'x_start': step['start_location']['lat'],
            'y_start': step['start_location']['lng'],
            'x_end': step['end_location']['lat'],
            'y_end': step['end_location']['lng'],
            'distance': step['distance']['value'],
            "duration": step['duration']['value']
        })
    df = pd.DataFrame(acc)
    df['velocity m/s'] = df['distance'] / df['duration']
    df['velocity km/h'] = df['velocity m/s'] * 3.6
    return df

print(preprocess_directions(directions_result))
    