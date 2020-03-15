# DMSS-dataset-exporter
Class that can be used to export the time series from a selection of the sensors from a given satellite.
This class takes care of normalization of the values and standardisation of the timing information.
Has a built-in ability to be dumped and loaded from a dump, as to allow a part of the dataset to be used on another cluster.

## Building a new dataset
The build function will export and preprocess the time-series data from the given sensors in the given mission.
After collecting all the necessary data, the timing will be standardized and the data will be homogenized through resampling.
The exporter.dataset object will get its sensors, timing and data arrays filled. The data field will be filled with an 2D array in which each internal array contains the value from each sensor at the time given by the value in the timing array with the same index.

```
exporter.build("mex", ["NACW0S00", "NAWG0051", "MG13G118", "NACW0S01", "NDMA5790", "NAWG0050", "MG13G119", "NDWDBT0M", "NDMA5740", "MG13G120", "NDWDBT0I", "NACAH030", "NDWDBT0G", "NACAH040", "NACAH050", "NDWDBT0K", "NDMA5715", "MG13G112", "MG13G102"])
# Builds a dataset with a selection of sensors from the mars express mission
```

## Dumping and loading
Use the dump function to save the build dataset in a given file.
The filename should use the .pickle extension.
After doing this you can move this pickle file to the machine where you want to use this dataset.
There you can use the load function with this filename.

```
exporter.dump(./dataset.pickle)
# Generates dataset.pickle file in the same folder as the Dataset_Exporter.py file

exporter.load(./dataset.pickle)
# Loads the previously saved dataset
```

## Normalization
Normalization is done like it would be done in real life. First the mean and standard deviation of each signal (only training samples) are calculated. The complete time series of each signal is normalized by subtracting the mean and dividing the result by the standard deviation. The size of the training set should therefore be given as an input to the normalize function.

The normalized data will be saved in the "normalized" array in the dataset object.
When you want to change the training set size, you can simply run normalize again with another size.

```
exporter.normalize(5000)
```

## Plotting signals
The exporter has the ability to plot the signals in its dataset. However these plots are very basic and are only used by me for taking a look at the used signals. Setting the argument normalized to True will make this function plot the normalized data, this argument is by default set to False.

```
exporter.plot()
# And/or
exporter.plot(normalized=True) 
```
## Accessing the data
The exporter builds a dataset object which can be accessed through the exporter. This object contains:
  * sensors: an array with the names of the sensors in the dataset
  * timing: an array with time standardized time points corresponding with the measurements of the sensors
  * data: a 2D array with for each time in the timing array a corresponding array with the measurements of the sensors in the same order as the names in the sensors array
  * normalized: same as data, but the data is normalized
  * training_size: used training_size during normalization
