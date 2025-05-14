#!/usr/bin/env python3
"""
Created on Fri Jun 2 14:17:59 2023

@author: joe.rolfe
"""
import json

import pandas as pd
import requests


def load_club_data(file, rows):
    """
    Loads club data from a CSV file.

    Arguments:
    - file (str): The file path of the CSV file.
    - rows (int): The number of rows to load from the file.

    Returns:
    - data (pd.DataFrame): The loaded club data as a pandas DataFrame.
    """
    data = pd.read_csv(file, nrows=rows)
    return data


# master doc has 1000 clubs in it, 350 will get you to step 4 and above.
data = load_club_data("postcodes_master.csv", 5)


def get_distance(point1: dict, point2: dict) -> tuple:
    """
    Gets the driving distance and duration between two points using
    http://project-osrm.org/docs/v5.10.0/api/#nearest-service

    Arguments:
    - point1 (dict): A dictionary representing the latitude and longitude of the first point.
    - point2 (dict): A dictionary representing the latitude and longitude of the second point.

    Returns:
    - tuple: A tuple containing the distance (in meters) and duration (in seconds) of the route.
    """
    url = (
        "http://router.project-osrm.org/route/v1/driving/"
        f"{point1['longitude']},{point1['latitude']};"
        f"{point2['longitude']},{point2['latitude']}"
        "?overview=false&alternatives=false"
    )
    r = requests.get(url)

    # get the distance from the returned values
    route = json.loads(r.content)["routes"][0]
    return (route["distance"], route["duration"])


def create_dist_array():
    """
    Creates an array of distances between all combinations of points in the loaded data.

    Returns:
    - dist_array (list): A list of tuples containing the origin index, destination index,
    duration (in seconds), and distance (in meters) between each pair of points.
    """
    dist_array = []
    for i, r in data.iterrows():
        point1 = {"latitude": r["latitude"], "longitude": r["longitude"]}
        for j, o in data[data.index != i].iterrows():
            point2 = {"latitude": o["latitude"], "longitude": o["longitude"]}
            dist, duration = get_distance(point1, point2)
            dist_array.append((i, j, duration, dist))

    return dist_array


dist_array = create_dist_array()


def create_distances_df():
    """
    Creates a DataFrame of distances between all combinations of points.

    Returns:
    - distances_df (pd.DataFrame): The DataFrame containing the distances between each pair of points,
    including origin and destination names, distance in miles, duration in HH:MM:SS format, and a fixture key.
    """

    distances_df = pd.DataFrame(dist_array, columns=["origin", "destination", "duration(s)", "distance(m)"])
    distances_df = distances_df.merge(data[["team"]], left_on="origin", right_index=True).rename(
        columns={"team": "origin_name"},
    )
    distances_df = distances_df.merge(data[["team"]], left_on="destination", right_index=True).rename(
        columns={"team": "destination_name"},
    )
    distances_df["distance(miles)"] = distances_df["distance(m)"] * 0.000621371
    distances_df["duration(hhmmss)"] = pd.to_datetime(distances_df["duration(s)"], unit="s").dt.strftime("%H:%M:%S")

    distances_df["fixture_key"] = (
        distances_df["destination_name"].str.strip() + "-" + distances_df["origin_name"].str.strip().astype(str)
    )

    return distances_df


journeys_df = create_distances_df()

journeys_df.to_csv("journeys_master.csv")
