#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/OBJ/fusion360/joint_assembly -name "model_*.obj")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh convert_fusion360_mesh.py $input --headless --mass 0.25 --collision-approximation meshSimplification