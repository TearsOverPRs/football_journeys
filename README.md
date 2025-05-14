## Football Journeys Project

## Project Summary

This Python project aims to calculate the driving distance between all combinations of football grounds based on their latitude and longitude coordinates. It utilizes various libraries, including pandas, requests, and json, to load the club data, fetch driving distance information from the OSRM API, and process the results.

## Project Structure

The project consists of the following main components:

`load_club_data`: This function loads football club data from a CSV file and returns it as a pandas DataFrame. The number of rows to load can be specified.

`get_distance`: This function retrieves the driving distance and duration between two points using the OSRM API. It takes in latitude and longitude coordinates of two points as dictionaries and returns a tuple containing the distance in meters and duration in seconds.

`create_dist_array`: This function creates an array of distances between all combinations of points. It iterates over the loaded club data and uses the get_distance function to calculate the distance and duration between each pair of points. The distances are stored in a list of tuples.

`create_distances_df`: This function creates a DataFrame of distances between all combinations of points. It takes the distance array obtained from create_dist_array and performs additional processing. The resulting DataFrame includes origin and destination names, distance in miles, duration in HH:MM:SS format, and a fixture key.

## Usage

Prepare the club data: The club data should be stored in a CSV file with columns including team, latitude, and longitude.

Load and process the data: Use the load_club_data function to load the club data from the CSV file. Specify the number of rows to load if desired. Then, the create_distances_df function can be used to calculate the driving distances between all combinations of points and create a DataFrame containing the results.

Save the results: The resulting distances DataFrame can be saved to a CSV file using the to_csv function.

Analyze the distances: The saved distances can be further analyzed or visualized to gain insights into the driving distances between football grounds.

## Conclusion

This project provides a framework for calculating driving distances between football grounds. It can be extended or customized to suit specific analysis or planning needs related to football match logistics, travel arrangements, or other geographical considerations.

## Developer Setup

### Setup Conda environment
```
conda create --name football_journeys python=3.10
conda activate football_journeys
```

### Install Dependencies
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Below code quality checks are implemented:
- Flake8: basic code quality checks
- Pylint: ensures PEP8 compliance and finds various code issues

```
pre-commit run --all-files
```
