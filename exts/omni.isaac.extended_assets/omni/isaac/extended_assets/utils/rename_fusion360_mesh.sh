#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/_fusion360/joint_assembly -name "*.obj")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh rename_fusion360_mesh.py $input