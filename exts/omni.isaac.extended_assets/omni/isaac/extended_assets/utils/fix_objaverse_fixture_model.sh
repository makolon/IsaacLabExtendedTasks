#!/bin/bash

find ../../../../data/_robocasa/fixtures -name "model.xml" | while read model_path; do
    # get directory name of model.xml
    dir_name=$(dirname "$model_path")
    dir_base=$(basename "$dir_name")
  
    input="$model_path"
    output="$dir_name/fixture.xml"

    echo $input
    echo $output

    # execute convert_mjcf.py in isaaclab
    /isaac-sim/python.sh fix_objaverse_fixture_model.py "$input" "$output"
done