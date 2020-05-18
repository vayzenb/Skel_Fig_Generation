import bpy
import numpy as np

ff = 0
#fig = [23, 31]
fig = [31]
SR = [0, 50]

#Assign tapers and bevels
bevelObj = "BalloonBevel"
taperObj = "ShrinkTaper"
mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
imgdir = "Images\\"
rawDir = "SpatialRelation\\"
viddir = "Videos\\"

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

		startRot = [[picPlane[pp], 0, 30]]


		endRot = [[picPlane[pp], 0,90]]
			
		rotName = ["Side"]

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



#Read CSV

for xx in range(0, len(SR)):
	coords = np.loadtxt('C:/Users/vayzenb/Desktop/Figure Generation/SpatialRelation/Figure_' + str(fig[ff]) + '.csv', delimiter = ',')


	segName = ['seg1', 'seg2', 'seg3']
	seg = [0,0,0]

	kk = 0
	for jj in range(0, 3997, 1998):
		currSegment = coords[jj:(jj+1998),:] 
		
		# create the Curve Datablock
		print(jj)
		curveData = bpy.data.curves.new(segName[kk], type='CURVE')
		curveData.dimensions = '3D'
		curveData.resolution_u = 2

		# map coords to spline
		polyline = curveData.splines.new('NURBS')
		polyline.points.add(len(currSegment))
		for i, coord in enumerate(currSegment):
			#x,y,z = currSegment
			polyline.points[i].co = (currSegment[i,0], currSegment[i,1], currSegment[i,2], 1)

		# create Object
		seg[kk] = bpy.data.objects.new(segName[kk], curveData)

		# attach to scene and validate context
		scn = bpy.context.scene
		scn.objects.link(seg[kk])
		scn.objects.active = seg[kk]
		seg[kk].select = False
		
		kk = kk + 1

	bpy.ops.object.select_all(action='DESELECT')

	#Connect all segments
	for ii in range(0,len(segName)):
		print(ii)
		bpy.data.objects[segName[ii]].select = True

	bpy.ops.object.join()

	#Rename object
	finalObj = bpy.context.selected_objects[0]
	bpy.context.object.name = "Figure_" + str(fig[ff]) + "_" + str(SR[xx])

	bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
	bpy.context.object.location = [0, 0, 0] #Reset location

	#Apply Bevel and Taper
	#bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj]
	#bpy.context.object.data.taper_object = bpy.data.objects[taperObj]
	bpy.context.object.data.resolution_u = 512


	#Set camera size
	bpy.context.scene.render.resolution_x = 1920
	bpy.context.scene.render.resolution_y = 1080

	#Change compression info
	bpy.data.scenes["Scene"].render.image_settings.compression = 25

	#Change color of object to red
	mat = bpy.data.materials.new(name="ColorMat") #Create new material

	finalObj.data.materials.append(mat) #add material to object
	bpy.context.object.active_material.diffuse_color = (1, 0, 0) #change color

	#World color
	bpy.context.scene.world.horizon_color = (.184, .184, .184)

	recordVid("Figure_" + str(fig[ff]), 'Bulge')

	finalObj.select = True
	#bpy.ops.wm.save_as_mainfile(filepath= mkdir + rawDir + "Figure_" + str(fig[ff]) + "_" + str(SR[xx] + ".blend") 
	
	bpy.ops.object.delete(use_global=False)
