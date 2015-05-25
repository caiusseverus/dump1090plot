#!/usr/bin/env python

import urllib
import re # for regular expressions

uf = urllib.urlopen('http://192.168.0.69:8080/dump1090/aircraft.json') # this is where the dump1090 data is stored
w = open("data.dat", 'a');

for line in uf.read(): # read source code
	w.write(line);

w.close()

