import bpy
import numpy as np
import os
from math import * 


#Assign tapers and bevels
bevelObj = "SkelBevel"
taperObj = "BalloonTaper"
mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
imgdir = "Images\\"
rawDir = "SpatialRelation\\"

f = 1
fig = [23, 31, 32, 266]
segNum = [0, 0, 0, 0]
splineNum = [0,0,0,0]
SR = [0, 10, 20, 30, 40, 50]



def takePic(objName, figNum):
	
	#Set file type
	bpy.context.scene.render.image_settings.file_format = "PNG"
	#Rotation coordinates
	picPlane = [0, 300, 90, 0]
	yRot = [0, 10, 30, 0]
	zRot = [[30, 60, 90], [30, 60, 90], [30, 60, 90], [30, 60, 90]]
	OGScale = bpy.context.object.scale
	
		#rotName = ["Front", "Top-Front", "Side-1", "Back", "Top-Back", "Side-2"]

	for kk in range(0, len(zRot[figNum])):
		
		picRot = [radians(picPlane[figNum]), radians(yRot[figNum]), radians(zRot[figNum][kk])]
		bpy.context.object.rotation_euler = picRot
		
		
		#Set file path for the render
		bpy.context.scene.render.filepath = mkdir + imgdir + objName + "_" + str(zRot[figNum][kk]) + ".png"
		bpy.context.object.scale = [.25, .25, .25]


		#Take the picture
		bpy.ops.render.render(write_still = True)
		bpy.context.object.rotation_euler = [0, 0, 0]
		bpy.context.object.scale = OGScale



#Load original MA file and calculate COM of target segment
OG = np.loadtxt('C:/Users/vayzenb/Desktop/Figure Generation/SpatialRelation/Figure_' + str(fig[f]) +  '.csv', delimiter = ',')
OGCOM = np.asarray([np.mean(OG[segNum[f]:(segNum[f] + 1998),0]), np.mean(OG[segNum[f]:(segNum[f] + 1998),1]), np.mean(OG[segNum[f]:(segNum[f] + 1998),2])])

#Select object
bpy.data.objects['Figure_' + str(fig[f])].select = True
obj = bpy.context.selected_objects[0]

#Remove bevel and Taper
bpy.context.object.data.bevel_object = None
bpy.context.object.data.taper_object = None

bpy.ops.object.mode_set(mode='EDIT')

#Select and seperate segment
obj.data.splines[splineNum[f]].bezier_points[0].select_control_point = True
obj.data.splines[splineNum[f]].bezier_points[1].select_control_point = True
bpy.ops.curve.separate()


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')


#Select new segment
bpy.data.objects['Figure_' + str(fig[f]) + '.001'].select = True
seg = bpy.context.selected_objects[0]
bpy.context.scene.objects.active = seg

#Set center of mass and record its location
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
blendCOM = bpy.context.object.location
blendCOM = np.asarray(blendCOM)

COMdiff = blendCOM - OGCOM


for jj in range(0, len(SR)):

	if jj > 0:
		print('ran?')
		
		#Select object
		bpy.data.objects['Figure_' + str(fig[f])].select = True
		obj = bpy.context.selected_objects[0]

		#Remove bevel and Taper
		bpy.context.object.data.bevel_object = None
		bpy.context.object.data.taper_object = None

		bpy.ops.object.mode_set(mode='EDIT')

		#Select and seperate segment
		obj.data.splines[0].bezier_points[0].select_control_point = True
		obj.data.splines[0].bezier_points[1].select_control_point = True
		bpy.ops.curve.separate()


		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')

		#Select new segment
		bpy.data.objects['Figure_' + str(fig[f]) + '.001'].select = True
		seg = bpy.context.selected_objects[0]
		bpy.context.scene.objects.active = seg

		#Set center of mass and record its location
		bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')


	coords = np.loadtxt('C:/Users/vayzenb/Desktop/Figure Generation/SpatialRelation/Figure_' + str(fig[f]) + '_' + str(SR[jj]) + '.csv', delimiter = ',')  
	newLOC = np.asarray([np.mean(coords[segNum[f]:(segNum[f] + 1998),0]), np.mean(coords[segNum[f]:(segNum[f] + 1998),1]), np.mean(coords[segNum[f]:(segNum[f] + 1998),2])]) + COMdiff

	bpy.context.object.location = newLOC
	bpy.ops.object.select_all(action='DESELECT')
	bpy.data.objects['Figure_' + str(fig[f]) + '.001'].select = True
	bpy.data.objects['Figure_' + str(fig[f])].select = True
	bpy.ops.object.join()
	bpy.context.object.name = "Figure_" + str(fig[f])

	bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

	#Apply Bevel and Taper
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj]
	bpy.context.object.data.taper_object = bpy.data.objects[taperObj]


		    #World color
	bpy.context.scene.world.horizon_color = (.184, .184, .184)

	takePic("Figure_" + str(fig[f]) + "_" + str(SR[jj]), f)





