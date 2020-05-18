import bpy 
import random
from math import * 
import numpy as np
import csv


def recordVid(objName,taper):
	bpy.data.objects[objName].select = True
	bpy.context.scene.objects.active = bpy.data.objects[objName]
	bpy.context.object.rotation_euler[2] = 0
	finalObj = bpy.context.selected_objects[0]

	lastFrame = 300
	#Set old context
	oldContext = bpy.context.area.type
	bpy.context.scene.frame_end = lastFrame #Set number of frames in the scene

	#Set file type
	bpy.context.scene.render.image_settings.file_format = "AVI_JPEG"
	
	picPlane = [0]
	
	for pp in range(0,len(picPlane)):

		startRot = [[picPlane[pp], 0, -30]]


		endRot = [[picPlane[pp], 0,30]]
			
		rotName = ["Front"]

		for kk in range(0, len(rotName)):
		
			if kk == 2:
				bpy.context.object.parent = bpy.data.objects["diagRot"]
				bpy.context.object.rotation_euler[0] = picPlane[pp]
				bpy.context.object.rotation_euler[2] = -0.785398
				bpy.data.objects[objName].select = False
				bpy.data.objects['diagRot'].select = True
				bpy.context.scene.objects.active = bpy.data.objects['diagRot']
				finalObj = bpy.context.selected_objects[0]
			elif kk == 3:
				bpy.context.object.parent = bpy.data.objects["diagRot"]
				bpy.context.object.rotation_euler[0] = picPlane[pp]
				bpy.context.object.rotation_euler[2] = 0.785398
				bpy.data.objects[objName].select = False
				bpy.data.objects['diagRot'].select = True
				bpy.context.scene.objects.active = bpy.data.objects['diagRot']
				finalObj = bpy.context.selected_objects[0] 

			print(picPlane[pp])
			
			#Go to first keyframe and set rotation
			bpy.context.object.rotation_euler = np.deg2rad(startRot[kk])
			#Insert keyframe for rotation
			finalObj.keyframe_insert('rotation_euler', frame = 0, group = "ABBA")

			#Go to mid keyframe and set rotation
			bpy.context.object.rotation_euler = np.deg2rad(endRot[kk])
			finalObj.keyframe_insert('rotation_euler', frame = lastFrame/2, group = "ABBA")

			#rotate back to the beginning
			bpy.context.object.rotation_euler = np.deg2rad(startRot[kk])
			finalObj.keyframe_insert('rotation_euler', frame = lastFrame, group = "ABBA")

			bpy.context.area.type = "GRAPH_EDITOR"
			bpy.ops.graph.extrapolation_type(type='LINEAR')
			bpy.ops.graph.handle_type(type = 'VECTOR')
			bpy.context.area.type = oldContext

			#Set format and file path for the render
			bpy.context.scene.render.antialiasing_samples = '11'
			bpy.context.scene.render.filepath = mkdir + viddir + objName +  taper + '_' + rotName[kk] + ".avi"

			#Render the video
			bpy.ops.render.render(animation=True)

			#Go to keyframe and delete keyframe
			finalObj.keyframe_delete("rotation_euler", frame = 0, group = "ABBA")
			finalObj.keyframe_delete("rotation_euler", frame = lastFrame/2, group = "ABBA")
			finalObj.keyframe_delete("rotation_euler", frame = lastFrame, group = "ABBA")

			bpy.data.objects[objName].select = True
			bpy.context.scene.objects.active = bpy.data.objects[objName]
			finalObj = bpy.context.selected_objects[0]
			bpy.context.object.rotation_euler = [0,0,0]
			bpy.context.object.parent = None
			
			#finalObj.keyframe_delete("rotation_euler", frame = 200, group = "ABBA")


def takePic(objName):
	
	#Set file type
	bpy.context.scene.render.image_settings.file_format = "PNG"
	#Rotation coordinates
	picRot = [[0, 0, -0.523598776], [0, -0.523598776, 0], [0, 0.785398163, 1.047197551], [0, 0, 2.617993878], [0, -0.523598776, 3.141592654], [0, 0.785398163, -2.094395102]]
	
	rotName = ["Front", "Top-Front", "Side-1", "Back", "Top-Back", "Side-2"]

	for kk in range(0, 6):
		bpy.context.object.rotation_euler = picRot[kk]
		
		#Set file path for the render
		bpy.context.scene.render.filepath = mkdir + imgdir + objName + taper + "_" + rotName[kk] + ".png"
	
		#Take the picture
		bpy.ops.render.render(write_still = True)
	
	bpy.context.scene.world.horizon_color = (.184, .184, .184)


#Go to render context
#bpy.context.space_data.context = 'RENDER'

#Enter the figures you want to render
figNum = [23]

#File paths for all the figures
mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
imgdir = "Images\\"
viddir = "Videos\\"
rawDir = "Raw Blend Files\\All\\Figure_" 

#Assign tapers and bevels
bevelObj = ["SkelBevel", "BalloonBevel"]
taperObj = ["BulgeTaper", "BalloonTaper", "ShrinkTaper", "WaveTaper"]



for ii in range(0, len(figNum)):
	#Opens file
	#bpy.ops.wm.open_mainfile(filepath= mkdir + rawDir + str(figNum[ii]) + ".blend")

	#selects object by name
	bpy.data.objects["Figure_" + str(figNum[ii])].select = True

	

	#Assign skel bevel and balloon taper
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[0]]
	bpy.context.object.data.taper_object = bpy.data.objects[taperObj[1]]
	bpy.context.object.data.resolution_u = 512 # set resolution
	bpy.context.scene.render.fps = 30 #Set FPS
	bpy.context.scene.frame_start = 0 #Set number of frames in the scene
	bpy.context.scene.world.horizon_color = (.184, .184, .184)

	#Take Skel pic
	#takePic("Figure_" + str(figNum[ii]) + "_" +"SkelTaper")
	#Take Skel video
	recordVid("Figure_" + str(figNum[ii]), "_" +"SkelTaper")
	#bpy.context.area.type = oldContext

	#Set bevel for remaining features
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[1]]

	for kk in range(0,len(taperObj)): #changed to two to ignore the shrink taper
		bpy.context.object.data.taper_object = bpy.data.objects[taperObj[kk]]
		
			#takePic("Figure_" + str(figNum) + "_" + taperObj[kk])
		recordVid("Figure_" + str(figNum[ii]),  "_" + taperObj[kk])
			#bpy.context.area.type = oldContext

