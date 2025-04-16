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

from code.gen_circuit_details import circuit_dict


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
    :return: floating value that denotes the distance between the two points in meters.
    TODO: make sure the return value makes sense in meters
    """
    distance_meters = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']
    return distance_meters

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

    :param mode:
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

def transport_time(track_A, track_B):
    """
    TODO: incomplete
    :param track_A:
    :param track_B:
    :return:
    """
    if track_A == "HQ":
        TrackB_lat = circuit_dict[trackB]["Latitude"]
        TrackB_long = circuit_dict[trackB]["Longitude"]
        dist = calculate_distance(HQ_lat = 52.0406, HQ_long= -0.7594, TrackB_lat, TrackB_long)

if __name__ == "__main__":
    print("PERT Testttt ")
    min_val, mode_val, max_val = 0.4, 0.8, 1.0
    for i in range(10):
        sample = pert_sample(min_val, mode_val, max_val)
        print(f"Sample {i+1}: {sample:.4f}")
    print("DONEEEEEEE")
    dist = calculate_distance(50.4372,5.9714, 47.58222, 19.25111)
    print(dist)