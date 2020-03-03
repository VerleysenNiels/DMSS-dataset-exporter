# DMSS-dataset-exporter
Class that can be used to export the time series from a selection of the sensors from a given satellite.
This class takes care of normalization of the values and standardisation of the timing information.
Has a built-in ability to be dumped and loaded from a dump, as to allow a part of the dataset to be used on another cluster.

## Building a new dataset
ToDo

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
ToDo

## Accessing the data
ToDo
