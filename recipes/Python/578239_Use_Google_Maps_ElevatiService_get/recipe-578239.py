#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json

def get_elevation(lat, lng, sensor=False):
    """
    Returns the elevation of a specific location on earth using the Google
    Maps API.

    @param lat (float): The latitude of the location in degrees. Latitudes can
    take any value between -90 and 90.
    @param lng (float): The longitude of the location in degrees. Longitudes
    can take any value between -180 and 180.
    @param sensor (boolean): This parameter is required by the Google maps API
    and indicates whether the application that requests the elevation data is
    using a sensor (such as a GPS device). Default value is 'False'.

    @return: A tuple (elevation, lat, lng, status):
      * elevation (float): The requested elevation in meters. If the location is
        on the sea floor the returned elevation has a negative value.
      * lat, lng (float): The latitude and longitude of the location (for testing
        purposes: must be equal to the input values).
      * status (str): Error code:
        "OK": the API request was successful.
        "INVALID_REQUEST": the API request was malformed.
        "OVER_QUERY_LIMIT": the requester has exceeded quota.
        "REQUEST_DENIED": the API did not complete the request, likely because
        of an invalid 'sensor' parameter.
        "UNKNOWN_ERROR": other error
      * If the error code 'status' is not 'OK' then all other members of the
        returned tuple are set to 'None'.

    @note: More information about the Google elevation API and its usage limits
    can be found in https://developers.google.com/maps/documentation/elevation/.
    
    @example:
    >>> round(get_elevation(-38.407, -25.297)[0], 2) == -3843.86
    True
    >>> round(get_elevation(37.32522, -104.98470)[0], 2) == 2934.24    
    True
    """
    ## build the url for the API call
    ELEVATION_BASE_URL = 'http://maps.google.com/maps/api/elevation/json'
    URL_PARAMS = "locations=%.7f,%.7f&sensor=%s" % (lat, lng, "true" if sensor else "false")
    url = ELEVATION_BASE_URL + "?" + URL_PARAMS

    ## make the call (ie. read the contents of the generated url) and decode the
    ## result (note: the result is in json format).
    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode())

    status = response["status"]
    if status == "OK":
        result = response["results"][0]
        elevation = float(result["elevation"])
        lat = float(result["location"]["lat"])
        lng = float(result["location"]["lng"])
    else:
        elevation = lat = lng = None
    return (elevation, lat, lng, status)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
