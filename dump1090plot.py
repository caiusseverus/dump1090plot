#!/usr/bin/env python

import re, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
	createfiles() 	# takes the full data.dat and breaks it down into a single file for each
					# plane (based off of icao hex code)
	plot()			# pull data from each file and make a 3d plot of each plane's path based
					# on the latitude, longitude, and altitude data they contain

def createfiles():
	dat = open("data.dat", 'rU');
	
	flag = { }  # create dictionary to be used to store hex codes. If a hex code has already been stored,
				# then the data file must exist for that code, so don't write it, just append to it
	i = 0;		# keys for dictionary (arbitrary, serve no purpose)
	
	for line in dat: # read source code
		hexdat = re.search('("hex":")([\w|\d]*)', line);
		if hexdat:
			hexdata = hexdat.group(2);
			flightdat = re.search('("flight":")([\w|\d]*)', line);
			if flightdat:
				flightdata = flightdat.group(2)
			latdat = re.search('("lat":)([-]*[\d]*\.[\d]*)', line);
			if latdat:
				latdata = latdat.group(2)
			else:
				latdata = "0.000000"
			londat = re.search('("lon":)([-]*[\d]*\.[\d]*)', line);
			if londat:
				londata = londat.group(2)
			else:
				londata = "0.000000"
			altdat = re.search('("altitude":)(\d*)', line);
			if altdat:
				altdata = altdat.group(2)
			else:
				altdata = 0
			trackdat = re.search('("track":)(\d*)', line);
			if trackdat:
				trackdata = trackdat.group(2)
			else:
				trackdata = 0
			speeddat = re.search('("speed":)(\d*)', line);
			if speeddat:
				speeddata = speeddat.group(2)
			else:
				speeddata = 0
	
			filename = "data/" + str(hexdata)# + ".dat"
	
			if str(hexdata) in flag.values(): 	# If a hex code has already been stored, then the data file
												# must exist for that code, so don't write it, just append
				wrfile = open(filename, 'a');
				wrfile.write("\n")
			else:
				wrfile = open(filename, 'w');
	
			wrfile.write(hexdata + "\n");
			if flightdat:
				wrfile.write(flightdata + "\n");
			else:
				flightdata = "abc123"
				wrfile.write(flightdata + "\n");

			# if latitude, longitude, or altitude data is a 0 (i.e. not present), don't write
			# any of the three - this cleans up the lists to eliminate bad data points when plotting		
			print "lat", latdata
			print "lon", londata
			print "alt", altdata
			print "line", line
			if altdata == "" or altdata < 0:
				altdata = "1"
			print "corrected alt", altdata	
			if float(latdata) != 0:
				if float(londata) != 0:
					if float(altdata) != 0:
						wrfile.write(latdata + "\n");
						wrfile.write(londata + "\n");
						wrfile.write(altdata + "\n");

			else:
				wrfile.write("\n");
				wrfile.write("\n");
				wrfile.write("\n");

			wrfile.write(str(trackdata) + "\n");
			wrfile.write(str(speeddata) + "\n");
			wrfile.close()
	
			flag[i] = str(hexdata) # update dictionary
			i +=1

def plot():

	############################################################################
	# This is where data is extracted from files and put into lists for plotting
	############################################################################

	allalts = { }
	alllats = { }
	alllons = { }
	allflights = { }
	counter = 0

	for file in os.listdir("data/"): # If an empty file named .DStore or something exists, it may not work - ?
		filename = "data/" + file;
		workingfile = open(filename, 'rU')


		worker = open(filename, 'rU'); 	# must open the file under a different name to count number of lines
		length = 0;
		for line in worker: 	# count number of lines in file to determine how long lists (below) should be
			length +=1;


		flightnumberlines = [x*8+1 for x in range(0, length)]
		latitudelines = [x*8+2 for x in range(0, length)]
		longitudelines = [x*8+3 for x in range(0, length)]
		altitudelines = [x*8+4 for x in range(0, length)]

		# initialize these as the empty list
		latlist = list()
		longlist = list()
		altlist = list()
		flightnumberlist = list()

		i = 0
		for line in workingfile:
			if i in latitudelines:
				latlist.append(line[0:len(line)-1])
			if i in longitudelines:
				longlist.append(line[0:len(line)-1])
			if i in altitudelines:
				altlist.append(line[0:len(line)-1])
			if i in flightnumberlines:
				flightnumberlist.append(line[0:len(line)-1])
			i += 1

		print altlist
		#print latlist
		#print longlist
		#print flightnumberlist

		# remove all null elements from the lists (planes that produced 0 complete position data points)
		altlist = map(float, filter(None, altlist))
		latlist = map(float, filter(None, latlist))
		longlist = map(float, filter(None, longlist))
		flightnumberlist = filter(None, flightnumberlist)

		allalts[counter] = altlist
		alllats[counter] = latlist
		alllons[counter] = longlist
		allflights[counter] = flightnumberlist

		counter += 1

		workingfile.close()
		worker.close()

	#print allalts
	#print alllats
	#print alllons
	#print allflights



	##########################################################################################################
	##########################################################################################################
	#			  		THIS IS WHERE PLOTTING OCCURS					 #
	##########################################################################################################
	##########################################################################################################



	#####################################################################
	#				THESE VALUES ARE USED TO FORMAT THE PLOTS			#
	#####################################################################

	# SET THESE LINES TO CURRENT LATITUDE AND LONGITUDE TO CENTER GRAPH
	currentlatitude = xx.xxxx	# Home is xx.xxxx
	currentlongitude = xx.xxxx	# Home is xx.xxxx

	# If the following is set to True it will plot from z = 0
	# If set to False it will plot from z = [minimum altitude] - 1000 ft
	plot_from_ground_level = False

	# The following is used to only plot flights under a certain altitude
	# Set this to float('inf') in order to see all flights
	only_plot_flights_under_this_altitude = float('inf') # to plot all: float('inf')

	# Setting this to True prints out the flight numbers for each plotted line
	# Setting this to False does not display flight numbers
	display_flight_number_labels = False

	# Set the following to True to plot planes WITHOUT flight number data
	# Set it to False to plot ONLY those planes WITH flight number data
	plot_planes_without_flight_numbers = False

	# If set to True planes with flight numbers containing only numbers
	# (e.g. 1653) will be displayed. If set to False then ONLY flight
	# numbers beginning with letters (e.g. UAL1653) will be displayed
	plot_planes_with_number_only_flight_numbers = True

	# Values used to change plot animation parameters are defined below #

	# If set to True all flight numbers will be printed to a document
	# titled flight_numbers.dat. If false, it will not make this file
	print_flight_number_file = False
	
	#####################################################################
	#####################################################################
	#####################################################################



	plt.ion() # this is necessary for animating (spinning in this case) the plot - it must stay here!!!
	
	fig = plt.figure(figsize=(15,9)) # this figure size fits well to macbook pro 13.3" screen
	ax = fig.add_subplot(111, projection='3d')



	minimumaltitude = filter(None, allalts.values())
	minimums = list() # initialize list of minimum altitudes of each plane
	for item in minimumaltitude:
		minimums.append(min(item))
	minimumaltitude = min(minimums) # find the absolute lowest altitude to be used as the bottom of the graph
	
	if plot_from_ground_level != True: # Described above, used to either plot from 0 up or [minalt - 1000] up
		floor = minimumaltitude - 1000
	else:
		floor = 0



	# these 2 circles are used to give an idea of the locations of the planes - each is ~120 miles in diameter
	xcircle = range(-100,101)
	xcircle = [float(item) / 100 for item in xcircle] # create a list from -2 to 2 with increment .1
	ycirclepos = [pow(pow(1,2) - (pow(item, 2)), .5) for item in xcircle]
	ycircleneg = [-pow(pow(1,2) - (pow(item, 2)), .5) for item in xcircle]
	ax.plot(xcircle, ycirclepos, floor, color='0.7')
	ax.plot(xcircle, ycircleneg, floor, color='0.7')
	# place the 120mi label at a 45 degree angle (in the NE quadrant of the plot)
	ax.text(-((pow(2,0.5)/2)-.05),(pow(2,0.5)/2)-.05,floor,"60 mi", fontsize=8, color='0.7')

	xcircle2 = range(-200,201)
	xcircle2 = [float(item) / 100 for item in xcircle2] # create a list from -2 to 2 with increment .1
	ycirclepos2 = [pow(pow(2,2) - (pow(item, 2)), .5) for item in xcircle2]
	ycircleneg2 = [-pow(pow(2,2) - (pow(item, 2)), .5) for item in xcircle2]
	ax.plot(xcircle2, ycirclepos2, floor, color='0.7')
	ax.plot(xcircle2, ycircleneg2, floor, color='0.7')
	# place the 120mi label at a 45 degree angle (in the NE quadrant of the plot)
	ax.text(-(pow(2,0.5)-.05),pow(2,0.5)-.05,floor,"120 mi", fontsize=8, color='0.7')


	all_plotted_lats = list()
	all_plotted_lons = list()
	all_plotted_alts = list()
	#feetperdegree = 362776; # to measure altitude in (roughly) degrees latitude
	for plot in range(len(allalts.values())):
		xx = alllats.values()[plot]
		xx = [item - currentlatitude for item in xx] # center the graph around current latitude
		xx = [-item for item in xx] # flip everything over the x axis so directions line up
									# Think about this like you're looking up at the planes
									# from below - positions of the cardinal directions are swapped
									# compared to looking down from above as you are in the plot
		yy = alllons.values()[plot]
		yy = [item - currentlongitude for item in yy] # center graph around current longitude
		zz = allalts.values()[plot]
		#zz = [item / feetperdegree for item in zz] # to measure altitude in (roughly) degrees latitude
		
		# obtain the flight number, if any
		flightnum = allflights.values()[plot]
		if len(flightnum) != 0:
			# If the flight number is only a number (e.g. 1653), then plot/don't plot according to setting
			if plot_planes_with_number_only_flight_numbers != True:
				chars = []
				for c in flightnum[0]:
					chars.append(c)
				letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
				 "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
				if chars[0] in letters:
					flightnum = flightnum
					if print_flight_number_file == True:
						flight_num_file = open("flight_numbers.dat", 'a')
						flight_num_file.write(flightnum[0] + "\n")
				else:
					flightnum = " "
			else:
				flightnum = flightnum
				if print_flight_number_file == True:
						flight_num_file = open("flight_numbers.dat", 'a')
						flight_num_file.write(flightnum[0] + "\n")
		else:
			flightnum = " "



		###############
		# plot the data
		###############

		# x-axis : latitude (degrees from current location, as set below)
		# y-axis : longitude (degrees from current location, as set below)
		# z-axis : altitude (ft)
		
		if len(xx) != 0: 				# don't attempt to plot empty lists
		
			# if the flight's minimum altitude is under the set threshold, plot the flight
			if only_plot_flights_under_this_altitude >= min(allalts.values()[plot]):
				if plot_planes_without_flight_numbers != True:	# this is set/described above
					if flightnum != " ":						# plot only planes WITH flight numbers
						ax.plot(xx, yy, zz)			# use ax.scatter(xx, yy, zz) for a scatter plot, etc.
						
						# The following statements keep track of all lats, lons, and alts that are PLOTTED
						# This is used for scaling the final plot, as described below
						for item in xx:
							all_plotted_lats.append(item)
						for item in yy:
							all_plotted_lons.append(item)
						for item in zz:
							all_plotted_alts.append(item)
						
						if display_flight_number_labels == True:
							ax.text(xx[0],yy[0],zz[0], " "+flightnum[0], fontsize=6)
				else:
					ax.plot(xx, yy, zz)			# use ax.scatter(xx, yy, zz) for a scatter plot, etc.
					
					# The following statements keep track of all lats, lons, and alts that are PLOTTED
					# This is used for scaling the final plot, as described below
					for item in xx:
						all_plotted_lats.append(item)
					for item in yy:
						all_plotted_lons.append(item)
					for item in zz:
						all_plotted_alts.append(item)
					
					if display_flight_number_labels == True:
						ax.text(xx[0],yy[0],zz[0], " "+flightnum[0], fontsize=6)


	# *** all_plotted_lats, all_plotted_alts, all_plotted_lons contain only values of PLOTTED planes *** #
	# The following obtains min and max latitude and longitude to be used in setting frame limits
	# of the plot - a makeshift way of scaling
	minimumlat =  min(all_plotted_lats)
	maximumlat =  max(all_plotted_lats)
	minimumlon =  min(all_plotted_lons)
	maximumlon =  max(all_plotted_lons)
	# The z-axis autoscale seems to be good enough, but these are here anyway for possible future use
	minimumalt =  min(all_plotted_alts)
	maximumalt =  max(all_plotted_alts)
	
	#ax.set_zlim(bottom=floor)

	# to keep the graph centered, the x and y limits must all be the same. So, I chose the largest
	# relative lat OR lon to be the absolute limit so that every point will stay within the frame
	# note: the z autoscale seems to be good enough
	s = max(abs(minimumlat), abs(minimumlon), abs(maximumlat), abs(maximumlon))
	ax.set_xlim(left=-s, right=s)		# x is latitude
	ax.set_ylim(bottom=-s, top=s)		# y is longitude

	#plt.show() # this is used for a static graph





	# make lines for x and y axes that extend slightly past the 120mi (2 degrees) marking circle
	xlimits = ax.get_xlim()
	ylimits = ax.get_ylim()
	ax.plot([float(xlimits[0])-.5, float(xlimits[1]+.5)], [0,0], [floor, floor], color='0.7')
	ax.plot([0,0], [float(ylimits[0])-.5, float(ylimits[1]+.5)], [floor, floor], color='0.7')

	# label the cardinal directions
	ax.text(0, s+.55, floor, " E", color='0.7')
	ax.text(0, -s-.55, floor, " W", color='0.7')
	ax.text(s+.55, 0, floor, " S", color='0.7')
	ax.text(-s-.55, 0, floor, " N", color='0.7')

	zticks = ax.get_zticks() # get the values that are displayed on the z axis by default
	ax.plot([0,0], [0,0], [floor,max(zticks)], color='0.7') # line for z axis


	# this prints a the default z-axis labels next to the new, centered, z axis
	itemnumber = 0
	for item in zticks:
		if (itemnumber % 2 != 0): # display every other label from the default z-axis labels
			ax.text(0,0,item," " + str(int(item)), fontsize=8, color='0.7') # z axis drawn at x=0, y=0
		itemnumber+=1

	plt.axis('off')			# turn ALL axes off



	# this is to rotate the plot at an elevation of 30 degrees through a full 360 degrees azimuthally
	# it quits after rotating 360 degrees (or whatever the upper limit of the range is)

	########################################################################################
	########################################################################################
	# ANIMATION PARAMETERS:
	speed = 1.5 # This is the speed at which the plot rotates. *** Higher numbers = slower ***
	revolutions = 3 # This is the number of revolutions that the plot will complete
	########################################################################################
	########################################################################################

	azimuths = range(0,int(((360*revolutions)*speed)+1))
	azimuths = [float(item) / speed for item in azimuths]

	f = 1
	for azimuth in azimuths:
		
		fname = "plot-" + str(f) + ".png" 
		ax.view_init(elev=45, azim=azimuth)
		plt.savefig(fname, format='png')
		f = f + 1






# This is the standard boilerplate that calls the main() function initially
if __name__ == '__main__':
	main()
