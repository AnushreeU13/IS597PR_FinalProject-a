"""
This code section is meant to create a dictionary
{'Melbourne Grand Prix Circuit': {'Latitude': ,
                                  'Longitude': ,
                                  'Distance_From_Previous_meters': ,
                                  'Distance_From_HQ_meters':
                                 },
 'Shanghai International Circuit': {... and so on
TODO: do we need to add Time_A_B also? if yes, then we'd assume some average speed, is that okay?

"""

from geographiclib.geodesic import Geodesic

# List of circuits with names and lat/lon
circuits = [
    ("Melbourne Grand Prix Circuit", -37.8497, 144.968),
    ("Shanghai International Circuit", 31.3389, 121.2189),
    ("Suzuka International Racing Course", 34.8431, 136.5419),
    ("Bahrain International Circuit", 26.0325, 50.5106),
    ("Jeddah Corniche Circuit", 21.6319, 39.1044),
    ("Miami International Autodrome", 25.9581, -80.2389),
    ("Autodromo Enzo e Dino Ferrari", 44.3439, 11.7167),
    ("Circuit de Monaco", 43.7347, 7.4206),
    ("Circuit de Barcelona-Catalunya", 41.57, 2.2611),
    ("Circuit Gilles-Villeneuve", 45.5000, -73.5228),
    ("Red Bull Ring", 47.2196, 14.7646),
    ("Silverstone Circuit", 52.0786, -1.0169),
    ("Circuit de Spa-Francorchamps", 50.4372, 5.9714),
    ("Hungaroring", 47.5822, 19.2511),
    ("Circuit Zandvoort", 52.3889, 4.5409),
    ("Autodromo Nazionale Monza", 45.6156, 9.2811),
    ("Baku City Circuit", 40.3725, 49.8533),
    ("Marina Bay Street Circuit", 1.2914, 103.8640),
    ("Circuit of the Americas", 30.1328, -97.6411),
    ("Autodromo Hermanos Rodriguez", 19.4042, -99.0907),
    ("Autodromo Jose Carlos Pace", -23.7036, -46.6997),
    ("Las Vegas Strip Circuit", 36.1147, -115.1728),
    ("Lusail International Circuit", 25.4892, 51.4531),
    ("Yas Marina Circuit", 24.4672, 54.6031)
]

# Red Bull HQ in Milton Keynes
hq_lat, hq_lon = 52.0406, -0.7594

# Create the dictionary
circuit_dict = {}

for i, (name, lat, lon) in enumerate(circuits):
    if i == 0:
        distance_prev = 0
    else:
        prev_lat, prev_lon = circuits[i - 1][1], circuits[i - 1][2]
        distance_prev = Geodesic.WGS84.Inverse(prev_lat, prev_lon, lat, lon)['s12']

    distance_hq = Geodesic.WGS84.Inverse(hq_lat, hq_lon, lat, lon)['s12']

    circuit_dict[name] = {
        "Latitude": lat,
        "Longitude": lon,
        "Distance_From_Previous_meters": distance_prev,
        "Distance_From_HQ_meters": distance_hq
    }

if __name__ == "__main__":
    print(circuit_dict)
