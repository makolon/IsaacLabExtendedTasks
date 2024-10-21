#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/USD/fixtures -name "*.usd" -not -name "instanceable_meshes.usd")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh recreate_usd.py $input