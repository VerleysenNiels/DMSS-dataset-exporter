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

import os
import pickle
from dmss.io.hdf5io import readorig


""" Very basic class that holds the exported dataset"""
class Dataset:
    def __init__(self):
        self.sensors = []
        self.timing = []
        self.data = []


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
        data = []
        zero = None     # This is the earliest timepoint
        start = None    # This is the earliest timepoint where every sensor started measuring
        end = None      # This is the smallest maxTime
        timestep = None
        # Start with reading the information from the sensors
        for sensor in sensors:
            # Read sensor data
            time, signal, info = readorig(sensor, mission=mission, timeInDays=True)
            data.append([time, signal])
            # Keep track of earliest measurement
            if zero is None:
                zero = info['minTime']
            elif zero > info['minTime']:
                zero = info['minTime']
            # Keep track of highest minTime
            if end is None:
                end = info['minTime']
            elif end < info['minTime']:
                end = info['minTime']
            # Keep track of lowest maxTime
            if end is None:
                end = info['maxTime']
            elif end > info['maxTime']:
                end = info['maxTime']
            # ToDo: check if same sampling rate
            if timestep is None:
                timestep = info['medianTimeStep']
            elif timestep != info['medianTimeStep']:
                print('WARNING DIFFERENT MEAN TIMESTEP DETECTED FOR SENSOR: ' + sensor)
                print('Expected: ' + str(timestep) + ' but got: ' + str(info['medianTimeStep']) + ' instead')

        # Startpoint of measurements is zero so we take measurements at index*timestep
        # Find total amount of timesteps extracted from the data
        length = round((end - start) / timestep)
        # Fill in timing information
        self.dataset.timing = [(start - zero) + i*timestep for i in range(0, length + 1)]

        # ToDo: Build a dataset object from this information


    # LOAD
    def load(self, file):
        with open(file, "rb") as pickle_in:
            self.dataset = pickle.load(pickle_in)

    # DUMP
    def dump(self, file):
        with open(file, "wb") as pickle_out:
            pickle.dump(self.dataset, pickle_out)

    # Normalize
    def normalize(self):
        print("ToDo")
        # ToDo: Determine mean and variance of the time series from each sensor
        # ToDo: Normalize by (X - mean) / variance
        # ToDo: Save normalized time series in self.dataset


# Test or run through here
if __name__ == '__main__':
    print("Test")
