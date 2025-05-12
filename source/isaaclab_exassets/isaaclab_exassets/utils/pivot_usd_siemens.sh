#!/bin/bash

# Store the paths of all object.xml files as a list in $input
input=$(find ../../../../data/Props/USD/siemens_gearbox/ -name "*.usd" ! -name "*non_metric.usd")

# Call convert_mjcf.py once, passing all input and corresponding output files
/isaac-sim/python.sh pivot_usd_siemens.py $input