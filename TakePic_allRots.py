import bpy 
import random
from math import * 
import numpy as np
import os
import re

def recordVid(objName):
	#Set file type
	bpy.context.scene.render.image_settings.file_format = "AVI_JPEG"	

	startRot = [[0, 0, -0.523598776], [0, -0.523598776, 0], [0, 0.785398163, 1.047197551], [0, 0, 2.617993878], [0, -0.523598776, 3.141592654], [0, 0.785398163, -2.094395102]]


	endRot = [[0, 0, 0.523598775598299], [0, 0.523598775598299, 0], [0, 0.785398163397448, 2.18166156499291], [0, 0, 3.66519142918809], [0, 0.523598775598299, 3.14159265358979], [0, 0.785398163397448, 2.18166156499291]]
		
	rotName = ["Front", "Top-Front", "Side-1", "Back", "Top-Back", "Side-2"]

	for kk in range(0, 6):
		
		#Go to first keyframe and set rotation
		bpy.context.object.rotation_euler = startRot[kk]
		#Insert keyframe for rotation
		finalObj.keyframe_insert('rotation_euler', frame = 1, group = "ABBA")

		#Go to end keyframe and set rotation
		bpy.context.object.rotation_euler = endRot[kk]
		finalObj.keyframe_insert('rotation_euler', frame = 120, group = "ABBA")

		#rotate back to the beginning
		bpy.context.object.rotation_euler = startRot[kk]
		finalObj.keyframe_insert('rotation_euler', frame = 240, group = "ABBA")

		
		#Set format and file path for the render
		bpy.context.scene.render.antialiasing_samples = '16'
		bpy.context.scene.render.filepath = mkdir + viddir + objName + "_" + rotName[kk] + ".avi"

		#Render the video
		bpy.ops.render.render(animation=True)

		#Go to keyframe and delete keyframe
		finalObj.keyframe_delete("rotation_euler", frame = 1, group = "ABBA")
		finalObj.keyframe_delete("rotation_euler", frame = 120, group = "ABBA")
		finalObj.keyframe_delete("rotation_euler", frame = 240, group = "ABBA")


def takePic(objName, figNum):
	
	#Set file type
	bpy.context.scene.render.image_settings.file_format = "PNG"
	#Rotation coordinates
	picPlane = [0]
	yRot = [10]
	zRot = [-90, -45, 0, 45, 90,]
	zRot = [-45,45]
	
		#rotName = ["Front", "Top-Front", "Side-1", "Back", "Top-Back", "Side-2"]

	for kk in range(0, len(zRot)):
		
		picRot = [radians(picPlane[0]), radians(yRot[0]), radians(zRot[kk])]
		bpy.context.object.rotation_euler = picRot
		
		
		#Set file path for the render
		bpy.context.scene.render.filepath = mkdir + imgdir + objName + "_" + str(zRot[kk]) + ".png"
	
		#Take the picture
		bpy.ops.render.render(write_still = True)

		#Rotate by 30 degrees (in radians)
		#picRot[2] = picRot[2] + 0.0174533 
	
	#bpy.context.object.rotation_euler = [0, 0.261799, 0]


#Go to render context
#bpy.context.space_data.context = 'RENDER'

#Enter the figures you want to render


#File paths for all the figures
mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
imgdir = "Images\\"
viddir = "Videos\\"
rawDir = "Raw Blend Files\\Figure_" 

#figNum = os.listdir(mkdir + rawDir)
#figNum =[23, 31, 32, 36, 39, 43, 44, 48, 56, 60, 61, 65, 71, 72, 76, 83, 85, 90, 100, 101, 103, 104, 106, 107, 108, 116, 117, 118, 234, 266]
figNum = [23,31,32,60,266]
startRot = [[170, 180, 90], [15, 30, 50], [25, 90, 270], [200,40,380], [30, 30, 80]]
#Assign tapers and bevels
bevelObj = ["SkelBevel", "BalloonBevel"]
taperObj = ["BalloonTaper", "BulgeTaper", "ShrinkTaper", "WaveTaper"]

blendReg = re.compile(r'.blend')
figureReg = re.compile(r'Figures')



for ii in range(0, len(figNum)):
	#Opens file
	#bpy.ops.wm.open_mainfile(filepath= mkdir + rawDir + figNum[ii])
	bpy.ops.wm.open_mainfile(filepath= mkdir + rawDir + str(figNum[ii]) + '.blend')

	#selects object by name
	bpy.data.objects['Figure_' + str(figNum[ii])].select = True
	bpy.context.object.scale = [0.25, .25, .25]
	bpy.context.object.rotation_euler = [radians(startRot[ii][0]),radians(startRot[ii][1]), radians(startRot[ii][2])]
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

	

	finalObj = bpy.context.selected_objects[0]

	#Assign skel bevel and balloon taper
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[0]]
	bpy.context.object.data.taper_object = bpy.data.objects[taperObj[0]]
	bpy.context.object.data.resolution_u = 512 # set resolution
	bpy.context.scene.render.fps = 30 #Set FPS

	#Set camera size
	bpy.context.scene.render.resolution_x = 1920
	bpy.context.scene.render.resolution_y = 1080

	#Change compression info
	bpy.data.scenes["Scene"].render.image_settings.compression = 25

	#Change color of background
	bpy.context.scene.world.horizon_color = (.184, .184, .184)

	#Take Skel pic
	#takePic(figureReg.sub('Figure',blendReg.sub('', figNum[ii])) + "_" +"SkelTaper")
	#takePic('Figure_' + str(figNum[ii]) + "_" +"SkelTaper", ii)
	
	#Take Skel video
	#recordVid("Figure_" + str(figNum[ii]) + "_" +"SkelTaper")

	#Set bevel for remaining features
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[1]]

	for kk in range(0,1):
		bpy.context.object.data.taper_object = bpy.data.objects[taperObj[kk]]
		takePic('Figure_' + str(figNum[ii]) + "_" + taperObj[kk], ii)
		

		#recordVid("Figure_" + str(figNum[ii]) + "_" + taperObj[kk])

