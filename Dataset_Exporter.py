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

    #BUILD
    def build(self, mission, sensors):
        print("ToDo")
        #ToDo: Load timing information and time series
        #ToDo: Standardize timing information and find point where all sensors start generating data
        #ToDo: Build a dataset object from this information

    #LOAD
    def load(self, file):
        with open(file, "rb") as pickle_in:
            self.dataset = pickle.load(pickle_in)

    #DUMP
    def dump(self, file):
        with open(file, "wb") as pickle_out:
            pickle.dump(self.dataset, pickle_out)

    #Normalize
    def normalize(self):
        print("ToDo")
        #ToDo: Determine mean and variance of the time series from each sensor
        #ToDo: Normalize by (X - mean) / variance
        #ToDo: Save normalized time series in self.dataset

# Test or run through here
if __name__ == '__main__':
    print("Test")