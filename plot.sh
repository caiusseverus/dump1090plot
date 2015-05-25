#!/bin/bash

rm -rf data &&
rm -rf flight_numbers.dat &&
mkdir data &&
python dump1090plot.py
