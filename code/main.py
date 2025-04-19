"""
IS597 Spring 2025 - Final Project
F1 Logistics using Monte Carlo Simulation: Core Functions
Author: Rahul Balasubramani(rahulb6) & Anushree Udhayakumar(au11)
"""

import random
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
import numpy as np
from gen_circuit_details import circuit_dict as circuit_dict


# PERT function to generate sample
def pert_sample(min_val, mode_val, max_val):
    """
    Generates a sample using PERT .
    TODO: can you provide citations for the above formulas?
    :param min_val: float, worst-case value
    :param mode_val: float, most likely value
    :param max_val: float, best-case value
    :return: float, a sample from the PERT distribution

    >>> s = pert_sample(0.4, 0.8, 1.0)
    >>> 0.4 <= s <= 1.0
    True
    """
    if not (min_val <= mode_val <= max_val):
        raise ValueError("Invalid PERT parameters")
    alpha  = 4 * (mode_val - min_val) / (max_val - min_val) + 1
    beta   = 4 * (max_val - mode_val) / (max_val - min_val) + 1
    sample = random.betavariate(alpha, beta)
    return min_val + sample * (max_val - min_val)

"""
#Calculate distance between 2 points
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km
"""
def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    This function takes inputs of coordinates(lat-long) and computes the great-circle distance between.
    :param lat1: Race location A latitude
    :param lon1: Race location A longitude
    :param lat2: Race location B latitude
    :param lon2: Race location B longitude
    :return: floating value that denotes the distance between the two points in km.
    TODO: make sure the return value makes sense in km
    """
    distance_meters = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']
    distance_km = distance_meters / 1000
    return distance_km

def simulate_crash()-> float:
    """
    This function is meant to return the total time it takes to fabricate a new part at the HQ, transport it to track location B
    :return: time, float
    """
    spare_status = None
    Car_status = None

    fabrication_time = fabrication()
    disturbance_delay = simulate_disturbance()
    breakdown_delay = simulate_breakdown()

    total_delay = fabrication_time + disturbance_delay + breakdown_delay + transport_time(HQ,Track_B)
    return round(total_delay,4)

def fabrication():
    """
    This function is meant to return the total time it takes to fabricate the spare part(s)
    :return:
    TODO: what distribution does fabrication follow?
    """
    fabrication_time = pert_sample(12, 18, 36)
    return fabrication_time

def simulate_breakdown(mode="road"):
    """
    This function simulates breakdown of the carrier -  trucks when roadways, cargo plane when airways
    :param mode: road or air
    :return:
    """
    if mode == "road":
        breakdown_prob = 0.02
        worst, highly_likely, best = 12, 3, 2  # hours - order is confusing
    elif mode == "air":
        breakdown_prob = 0.02
        worst, highly_likely, best = 12, 4, 3  # hours
    else:
        raise ValueError("Mode must be 'road' or 'air'")

    # Check if a breakdown occurs
    if np.random.binomial(1, breakdown_prob):
        delay = pert_sample(worst, highly_likely, best)
        return round(delay, 4)
    return 0


def transport_time(loc_A, loc_B, mode="road"):
    """
    Calculates transport time (in hours) from loc_A to loc_B.
    Uses PERT-sampled speed and geodesic distance.

    :param loc_A: 'HQ' or name of circuit A
    :param loc_B: name of circuit B
    :param mode: 'road' (default), or 'air' if needed later
    :return: time in hours (float)
    """
    # HQ coordinates (Milton Keynes)
    hq_lat, hq_lon = 52.0406, -0.7594

    # Get coordinates for location A
    if loc_A == "HQ":
        lat_A, lon_A = hq_lat, hq_lon
    else:
        lat_A = circuit_dict[loc_A]["Latitude"]
        lon_A = circuit_dict[loc_A]["Longitude"]

    # Get coordinates for location B
    lat_B = circuit_dict[loc_B]["Latitude"]
    lon_B = circuit_dict[loc_B]["Longitude"]

    # Calculate distance in kilometers
    distance_km = calculate_distance(lat_A, lon_A, lat_B, lon_B)

    # Sample speed using PERT
    if mode == "road":
        speed_kmph = pert_sample(48, 80, 100) #we have citation for this
    elif mode == "air":
        speed_kmph = pert_sample(600, 700, 800)  #no citation for this
    else:
        raise ValueError("Unsupported mode: use 'road' or 'air'.")

    # Time = distance / speed
    travel_time_hrs = distance_km / speed_kmph
    return round(travel_time_hrs, 2)


def simulate_disturbance():
    """
    Simulates if a disturbance occurs and computes its delay. Returns 0 if no disturbance occurs.
    If it does, calculates delay = duration × severity factor.
    """
    disturbance_prob = 0.1  # 10% chance - put this in the simulator()

    # Check if disturbance occurs
    if np.random.binomial(1, disturbance_prob):
        duration = pert_sample(2, 6, 48)  # best-mostlikely-worstDuration in hours
        severity = pert_sample(0.1,0.2, 1)  # Severity as a multiplier
        delay = duration * severity
        return round(delay, 2)

    return 0


if __name__ == "__main__":
