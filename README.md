<img alt="Laputa, The Flying Island"
     src="https://upload.wikimedia.org/wikipedia/commons/4/44/Laputa_-_Grandville.jpg"
     align="right"
/>

# trajpred
Trajectory predictions implemented in python

## Architecture

### Notebooks

Jupyter notebooks are used for experimenting, measurements and generating simple visualizations.

### Tools

* [Predictor](./tools/predictor/) &mdash; CLI tool for generating predictions and reports
* [Preprocessor](./tools/preprocessor/) &mdash; Python script that downloads, verifies and extracts the dataset.
* [Visualizer](./tools/visualizer/) &mdash; Simple tool written in ClojureScript for visualizing trajectories in the browser.

### Utils

[`utils`](./utils/) contains all the helper functions used in the Jupyter notebooks.

## Predictions

### Dataset
The dataset that is used is [Mopsi Routes 2019 dataset](http://cs.uef.fi/mopsi/routes/2019/). It contains 2,484 routes recorded by 10 users performing various activities such as walking, cycling, hiking, jogging, orienteering, skiing, driving, traveling by bus, train or boat.

### Methods
Every method works by first splitting the trajectory into two parts and then using the head part as the learning resource and the tail as the *ground truth*.

#### Bullet method
*The bullet method* uses only the last two coordinates of the head of the trajectory because it is supposed to be a simple method for later comparison.

#### Random tail method
*The random tail method* collects overlapping trajectories from the history and picks one randomly. The random tail is used as the prediction by selecting the right amount of coordinates from it.

## References

* [Data-driven Trajectory Prediction and Spatial Variability of Prediction Performance in Mari-time Location Based Services](https://www.zora.uzh.ch/id/eprint/177490/1/LBS_2019.pdf)
