# Mean Shift Viewer
A simple GUI to explore the capabilities of [pymeanshift](https://github.com/fjean/pymeanshift) library.

![alt text](https://github.com/mauricioprod/MeanShift_Viewer/blob/main/figs/interface_example.png?raw=true)

----
## Installation

### Requirements
* Windows or Linux.
* [Conda](https://conda.io/docs/user-guide/install/index.html): package, dependency and environment management.
* Packages in [environment.yml](https://github.com/mauricioprod/MeanShift_Viewer/blob/main/environment.yml).

### Guide

1. Open the terminal;
2. Download and unzip the source [code](https://github.com/mauricioprod/MeanShift_Viewer/archive/main.zip);
3. Create the `msui` virtual environment by running
the following command `conda env create -n msui -f environment.yml`;
4. Activate your environment by typing `$ source activate msui`;
To deactivate the environment type in `$ source deactivate`.
NOTE: Remember to always activate the environment before running the code;
5. Launch the software `$ python meanshift.py`.

----
## Usage
To use the real-time application:

1. Load the image by clicking on `Load image` button.
2. Define the `Spatial radius`, `Range radius` and `Minimum density` pymeanshift parameters.
3. Click on `Apply` button to see the result (If you are not satisfied, come back to tunne the pymeanshift parameters and then click on `Apply` to see the change).
4. Click on `Save` button to save the segmented image (It saves in the same folder of the orginal image).
