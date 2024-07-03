#!/bin/bash
modules=('boot' 'config' 'hardware' 'networking' 'programs' 'system' 'virtualisation' 'security')
# Loop through each defined module type
for module in "${modules[@]}"
do
  # Construct the output filename
  output_file="${module}.json"
  
  # Call the Python program with the current letter and output file
  python src/main.py --channel unstable --options --size 10000 "${module}." --output "data/other-modules/${output_file}"
done
