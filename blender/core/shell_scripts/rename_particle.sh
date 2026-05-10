#!/bin/bash

set -e

DATA_DIR="../../../../data_1000/particle"

i=1
for f in "$DATA_DIR"/IAM_V_M_V_*.txt; do
	mv "$f" "$DATA_DIR/particle-$i.csv"
	((i++))
done

# Remove header line
sed -i '1d' "$DATA_DIR"/particle-*.csv

echo "Particle files renamed and cleaned successfully."
