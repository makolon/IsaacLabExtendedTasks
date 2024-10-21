#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find . -name "mobility_texture_gapartnet.urdf")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh convert_partnet_urdf.py $input --headless --make-instanceable