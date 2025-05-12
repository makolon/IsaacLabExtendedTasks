#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/USD/ -name "*.usd")

# Call convert_objaverse_fixture_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh add_texture.py $input