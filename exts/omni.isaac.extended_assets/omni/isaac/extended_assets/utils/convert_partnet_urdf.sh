#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input_urdf=$(find ../../../../data/Props/URDF/gapartnet -name "mobility_texture_gapartnet.urdf")
input_meta=$(find ../../../../data/Props/URDF/gapartnet -name "result.json")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh convert_partnet_urdf.py "$input_urdf" "$input_meta" --headless