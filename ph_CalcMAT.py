import bpy 
import random
from math import * 
import numpy as np
import csv
import os



####################################
#This section calculates the points of the curve
def interpBez3(bp0, t, bp3):

	return interpBez3_(bp0.co, bp0.handle_right, bp3.handle_left, bp3.co, t)

def interpBez3_(p0, p1, p2, p3, t):
	r = 1-t
	return (r*r*r*p0 +
			3*r*r*t*p1 +
			3*r*t*t*p2 +
			t*t*t*p3)

def mission1(obj, t,spl):
	points = []
	i1 = floor(t)

	curve = obj.data

	for ii in range(0,2):
		bp1 = curve.splines[spl].bezier_points[i1]
		bp2 = curve.splines[spl].bezier_points[i1+1]
	
			#This caluclates the points of the curve in "object space" then converts it to "world space"
		tempPoints = obj.matrix_world * interpBez3(bp1, t-i1, bp2)
		points.append(tempPoints)

	return points

def calcCurvePoints(spl):
	points = []
	k = 0.000
	
	#Calculate a 1000 points of the curve by steps of .001
	for jj in range(0, 999):
		points.append(mission1(bpy.context.active_object, k, spl))
		k += 0.001
	
	return points

mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
rawDir = "Raw Blend Files\\all\\" 
axDir = "Axes\\"
figs = os.listdir(mkdir + rawDir)


for kk in range(0,len(figs) + 1):

	if figs[kk][-5:] == 'blend':
		bpy.ops.wm.open_mainfile(filepath= mkdir + rawDir + figs[kk])

		#go to object mode, recenter, and deselect all
		bpy.ops.object.select_all(action='DESELECT')

		bpy.data.objects[figs[kk][:-6]].select = True

		bpy.ops.object.mode_set(mode='EDIT')




		points = []

		for ii in range(0,3):
			k = 0.000

			#Calculate a 1000 points of the curve by steps of .001
			for jj in range(0, 999):
				points.extend(mission1(bpy.context.active_object, k, ii))
				k += 0.001
		#finalPoints = []
		#for jj in range(0,3):
		#   finalPoints.append = (calcCurvePoints(jj))
		points = np.asarray(points)
		print(points.shape)
		print(points)

		
		np.savetxt(mkdir + axDir + figs[kk][:-6] + ".csv", points, delimiter=",") 