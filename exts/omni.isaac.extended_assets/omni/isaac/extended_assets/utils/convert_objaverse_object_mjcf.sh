#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/MJCF/objaverse/objects -name "object.xml")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh convert_objaverse_object_mjcf.py $input --headless --make-instanceable --import-sites