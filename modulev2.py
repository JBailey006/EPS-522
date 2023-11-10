## Module for class lab exercise
## David A. Giovannetti-Nazario


import numpy as np
import pandas as pd
import os
import glob

## Function 1 - returns least-squares velocity and uncertainty for timeseries data
def fit_timeseries(tlist, ylist):
    A = np.vstack([tlist, np.ones(len(tlist))]).T
    m, c = np.linalg.lstsq(A, ylist, rcond=None)[0]
    velocity = m * 1000
    residuals = ylist - (m * tlist + c)
    uncertainty = np.sqrt(np.sum(residuals ** 2) / (len(tlist) - 2)) * 1000
    return velocity, uncertainty


## Function 2 - uses Function 1 to return the N, E, and Up components of velocity for timeseries data

def fit_velocities(filename):
    data = pd.read_csv(filename, delim_whitespace=True)
    velocity_e, uncertainty_e = fit_timeseries(data['yyyy.yyyy'], data['__east(m)'])
    velocity_n, uncertainty_n = fit_timeseries(data['yyyy.yyyy'], data['_north(m)'])
    velocity_u, uncertainty_u = fit_timeseries(data['yyyy.yyyy'], data['____up(m)'])
    return velocity_e, uncertainty_e, velocity_n, uncertainty_n, velocity_u, uncertainty_u


## Function 3 - returns the average coordinates and elevation for timeseries data site over time

def get_coordinates(filename):
    data = pd.read_csv(filename, delim_whitespace=True)
    latitude = data['_latitude(deg)']
    longitude = data['_longitude(deg)']
    elevation = data['__height(m)']
    
    ave_latitude = latitude.mean()
    ave_longitude = longitude.mean()
    ave_elevation = elevation.mean()
    
    return ave_latitude, ave_longitude, ave_elevation


## Function 4 - Modified to accept a type parameter

def fit_all_velocities(folder_name, file_pattern, data_type):
    results = []
    for file in glob.glob(os.path.join(folder_name, file_pattern)):
        site_name = os.path.splitext(os.path.basename(file))[0]
        if data_type == 'GNSS':
            velocity_e, uncertainty_e, velocity_n, uncertainty_n, velocity_u, uncertainty_u = fit_velocities(file)
            ave_latitude, ave_longitude, ave_elevation = get_coordinates(file)
        
            results.append({
                'Site Name': site_name,
                'Average Latitude': ave_latitude,
                'Average Longitude': ave_longitude,
                'Average Elevation': ave_elevation,
                'East Velocity (mm/year)': velocity_e,
                'East Uncertainty (mm/year)': uncertainty_e,
                'North Velocity (mm/year)': velocity_n,
                'North Uncertainty (mm/year)': uncertainty_n,
                'Up Velocity (mm/year)': velocity_u,
                'Up Uncertainty (mm/year)': uncertainty_u,
            })
        elif data_type == 'tide':
            data = pd.read_csv(file, sep=';', header=None)
            tlist = data.iloc[:, 0]
            ylist = data.iloc[:, 1]
            #identify only the good data points and get rid of the rest, using logical indexing
            okdata = data.iloc[:, 1] != -99999
            tlist=tlist[okdata]
            ylist=ylist[okdata]
            velocity, uncertainty = fit_timeseries(tlist, ylist)
            results.append({
                #'Site Name': site_name,
                'Rate of change (mm/year)': velocity/1000
            })
        else:
            raise ValueError("Unsupported data_type. Use 'GNSS' or 'tide'.")

    results_df = pd.DataFrame(results)

    return results_df

## Function 5 - Uses Function 1 to calculate rate of change of sea-level timeseries

def fit_tide_gauge(data):
    tlist = data.iloc[:, 0] != -9999
    ylist = data.iloc[:, 1] != -9999
    velocity, uncertainty = fit_timeseries(tlist, ylist)
    return velocity, uncertainty
