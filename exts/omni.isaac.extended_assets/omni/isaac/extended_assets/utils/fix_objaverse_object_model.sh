#!/bin/bash

find ../../../../data/_robocasa/objects/objaverse -name "model.xml" | while read model_path; do
    # get directory name of model.xml
    dir_name=$(dirname "$model_path")
    dir_base=$(basename "$dir_name")
  
    input="$model_path"
    output="$dir_name/object.xml"

    echo $input
    echo $output

    # execute convert_mjcf.py in isaaclab
    /isaac-sim/python.sh fix_objaverse_object_model.py "$input" "$output"
done