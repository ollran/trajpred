<img alt="Laputa, The Flying Island"
     src="https://upload.wikimedia.org/wikipedia/commons/4/44/Laputa_-_Grandville.jpg"
     align="right"
/>

# trajpred
Trajectory predictions implemented in python

## Dataset
The dataset that is used is [Mopsi Routes 2019 dataset](http://cs.uef.fi/mopsi/routes/2019/). It contains 2,484 routes recorded by 10 users performing various activities such as walking, cycling, hiking, jogging, orienteering, skiing, driving, traveling by bus, train or boat.

## Methods
Every method works by first splitting the trajectory into two parts and then using the head part as the learning resource and the tail as the *ground truth*.

### Bullet method
*The bullet method* uses only the last two coordinates of the head of the trajectory because it is supposed to be a simple method for later comparison.

### Random tail
*The random tail method* collects overlapping trajectories from the history and picks one randomly. The random tail is used as the prediction by selecting the right amount of coordinates from it.
