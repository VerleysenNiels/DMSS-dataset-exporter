#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Mar 3 13:46:38 2020

@author: Niels Verleysen

Class to export and transform time series of a given set of sensors of a given mission to a usable dataset.
General procedure as follows:
    1. Build dataset with list of wanted sensors and name of the satellite
        WARNING: This should be done on a machine with access to /STER/dmss/data
    2. Dump the dataset and move the dumped file to the machine where it will be used
    3. Load this file on the new machine when you need it
    Optionally the time series can be normalized as well

For more information check out the readme.
"""

import pickle
import numpy as np
from dmss.io.hdf5io import readorig
import matplotlib.pyplot as plt


""" Very basic class that holds the exported dataset"""
class Dataset:
    def __init__(self):
        self.sensors = []
        self.timing = []
        self.missing = []  # Binary indicators, 0 when value was measured and 1 when it was not
        self.data = []
        self.normalized = []
        self.training_size = None
        self.start = 0     # Gives start index (skipping long gaps)

""" Main class to be used to build/dump/load/normalize the dataset """
class Dataset_Exporter:

    def __init__(self):
        self.dataset = None

    # BUILD
    def build(self, mission, sensors):
        # Init dataset object
        self.dataset = Dataset()
        self.dataset.sensors = sensors
        # Define variables for processing the sensor information
        data = {}

        # Start with reading the information from the sensors
        for sensor in sensors:
            # Read sensor data
            time, signal, info = readorig(sensor, mission=mission, timeInDays=True)
            data[sensor] = {'time': time, 'signal': signal}

        # Determine timing variables
        start = max([data[name]['time'][0] for name in sensors])  # This is the earliest timepoint where every sensor started measuring
        end = min([data[name]['time'][-1] for name in sensors])  # This is the smallest maxTime
        timestep = np.median([np.median(np.diff(data[name]['time'])) for name in sensors])

        # Fill in timing information
        self.dataset.timing = np.arange(start, end, timestep)
        
        #Check for gaps
        for sensor in sensors:
            missing = []
            i = 0
            while data[sensor]['time'][i] < start:
                i += 1
            i += 1
            for time_index in range(i, len(data[sensor]['time'])):
                measured_timestep = data[sensor]['time'][time_index] - data[sensor]['time'][time_index - 1]

                # Fill in binary indicator variable for gaps
                if measured_timestep > 1.2 * timestep:
                    missing.append(1)
                else:
                    missing.append(0)

                # If measured gap is too large, don't use it
                if measured_timestep > 50 * timestep:
                    print("Gap found for sensor: " + sensor + " at time: " + str(data[sensor]['time'][time_index - 1]) + " expected timestep to be " + str(timestep) + " but got " + str(measured_timestep) + " instead.")
                    if self.dataset.start < data[sensor]['time'][time_index]:
                        print(str(len(self.dataset.timing)))
                        self.dataset.start = int(round((data[sensor]['time'][time_index] - start)/timestep))
                        print('New starting time: ' + str(self.dataset.timing[self.dataset.start]))

                # Add binary indicators for missing values of this sensor to the dataset
                self.dataset.missing.append(missing)

        # Transpose the list with binary indicators to have the same structure as the values
        self.dataset.missing = np.transpose(self.dataset.missing)

        # Homogenize timesteps by resampling the data (interpolation)
        self.dataset.data = []
        [self.dataset.data.append(np.interp(self.dataset.timing, data[sensor]['time'], data[sensor]['signal'])) for sensor in sensors]
        self.dataset.data = np.transpose(self.dataset.data)


    # LOAD
    def load(self, file):
        with open(file, "rb") as pickle_in:
            self.dataset = pickle.load(pickle_in)

    # DUMP
    def dump(self, file):
        with open(file, "wb") as pickle_out:
            pickle.dump(self.dataset, pickle_out)

    def plot(self, normalized=False):
        if normalized:
            data = self.dataset.normalized[self.dataset.start:-1]
        else:
            data = self.dataset.data[self.dataset.start:-1]

        for i in range(0, len(self.dataset.sensors)):
            plt.plot(self.dataset.timing[self.dataset.start:-1], np.transpose(data)[i])
            plt.ylabel("Signal: " + self.dataset.sensors[i])
            plt.xlabel("Time (days)")
            plt.show()

    # ToDo: Check if this works
    # Normalize
    def normalize(self, training_size):
        # Determine which portion of the data will be used for training
        self.dataset.training_size = training_size
        self.dataset.normalized = []
        for signal in np.transpose(self.dataset.data):
            # Determine mean and standard deviation for training set
            mean = np.mean(signal[0:training_size-1])
            deviation = np.std(signal[0:training_size-1])
            norm = lambda x: (x - mean)/deviation
            self.dataset.normalized.append(norm(signal))
        self.dataset.normalized = np.transpose(self.dataset.normalized)

# Test or run through here
if __name__ == '__main__':
    exporter = Dataset_Exporter()
    #exporter.load("Dataset.pickle")
    exporter.build("mex", ["NACW0S00", "NAWG0051", "NACW0S01", "NDMA5790", "NAWG0050", "NDWDBT0M", "NDMA5740", "NDWDBT0I", "NACAH030", "NDWDBT0G", "NACAH040", "NACAH050", "NDWDBT0K", "NDMA5715"])
    #exporter.plot()
    #print(exporter.dataset.sensors)
    #print(exporter.dataset.timing)
    exporter.normalize(10000)
    exporter.plot(normalized=True)
    exporter.dump("Dataset.pickle")

