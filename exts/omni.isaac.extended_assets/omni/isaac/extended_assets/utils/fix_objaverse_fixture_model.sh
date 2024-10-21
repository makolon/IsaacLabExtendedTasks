#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/MJCF/objaverse/fixtures -name "*.xml")

# Call fix_objaverse_fixture_model.py once, passing all input and corresponding output files
/isaac-sim/python.sh fix_objaverse_fixture_model.py $input
