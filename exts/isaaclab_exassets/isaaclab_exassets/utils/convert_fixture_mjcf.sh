#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/MJCF/fixtures -name "*_fixed.xml")

# Call convert_objaverse_fixture_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh convert_fixture_mjcf.py $input --make-instanceable --fix-base --import-sites