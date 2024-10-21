#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/MJCF/fixtures -name "model.xml")

# Call fix_fixture_model.py once, passing all input and corresponding output files
/isaac-sim/python.sh fix_fixture_model.py $input
