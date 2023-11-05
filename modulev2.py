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
    if np.array_equal(ylist, np.array(filename['__east(m)'])):
        velocity_e, uncertainty_e = fit_timeseries(tlist, ylist)
        north = np.array(data['_north(m)'])
        velocity_n, uncertainty_n = fit_timeseries(tlist, north)
        up = np.array(data['____up(m)'])
        velocity_u, uncertainty_u = fit_timeseries(tlist, up)
    elif np.array_equal(ylist, np.array(filename['_north(m)'])):
        velocity_n, uncertainty_n = fit_timeseries(tlist, ylist)
        east = np.array(data['__east(m)'])
        velocity_e, uncertainty_e = fit_timeseries(tlist, east)
        up = np.array(data['____up(m)'])
        velocity_u, uncertainty_u = fit_timeseries(tlist, up)
    elif np.array_equal(ylsit, np.array(filename['____up(m)'])):
        velocity_u, uncertainty_u = fit_timeseries(tlist, ylist)
        east = np.array(data['__east(m)'])
        velocity_e, uncertainty_e = fit_timeseries(tlist, east)
        north = np.array(data['_north(m)'])
        velocity_n, uncertainty_n = fit_timeseries(tlist, north)
    else:
        raise ValueError("Something wrong with ylist parameter")
        
    return velocity_e, uncertainty_e, velocity_n, uncertainty_n, velocity_u, uncertainty_u


## Function 3 - returns the average coordinates and elevation for timeseries data site over time

def get_coordinates(filename):
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
            velocity, uncertainty = fit_timeseries(tlist, ylist)
            ave_latitude, ave_longitude, ave_elevation = get_coordinates(filename)
        
            results.append({
                'Site Name': site_name,
                'Average Latitude': ave_latitude,
                'Average Longitude': ave_longitude,
                'Average Elevation': ave_elevation,
                'Velocity (mm/year)': velocity,
                'Uncertainty (mm/year)': uncertainty
            })
        elif data_type == 'tide':
            data = pd.read_csv(file, delim_whitespace=True, header=None)
            tlist = data.iloc[:, 0] != -9999
            ylist = data.iloc[:, 1] != -9999
            
            velocity, uncertainty = fit_timeseries(tlist, ylist)
            results.append({
                #'Site Name': site_name,
                'Rate of change (mm/year)': velocity
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