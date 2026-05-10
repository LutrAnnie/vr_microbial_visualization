#!/bin/bash

# Stop if something fails
set -e

DATA_DIR="../../../../data_1000/grid"

i=1
for f in "$DATA_DIR"/IAM_B_C_*.txt; do
	mv "$f" "$DATA_DIR/grid-$i.csv"
	((i++))
done

# Remove header line from each file
sed -i '1d' "$DATA_DIR"/grid-*.csv

echo "Grid files renamed and cleaned successfully."
