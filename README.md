<img alt="Laputa, The Flying Island"
     src="https://upload.wikimedia.org/wikipedia/commons/4/44/Laputa_-_Grandville.jpg"
     align="right"
/>

# trajpred
Trajectory predictions implemented in python

## Methods
Every method works by first splitting the trajectory into two parts and then using the head part as the learning resource and the tail as the *ground truth*.

### Bullet method
*The bullet method* uses only the last two coordinates of the head of the trajectory because it is supposed to be a simple method for later comparison.
