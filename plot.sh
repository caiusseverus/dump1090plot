#!/bin/bash

rm -rf data &&
rm -rf flight_numbers.dat &&
rm *.png
mkdir data &&
awk '/hex/' rawdata.dat | awk '/altitude/ && /lat/ && /lon/' > data.dat &&
sed -i 's/^ *//' data.dat &&
sed -i '/ground/d' data.dat &&
python2 dump1090plot.py
