#
# This file contains auxiliary functions that are not intended to be
# imported directly by the end user.
# The main function `get_stations_by_radius` uses them
# to perform its calculations.
#

import math
import numpy as np

R_EARTH_KM = 6371.0088

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points (in km) using the Haversine formula.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R_EARTH_KM * c

