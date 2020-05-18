import bpy
import numpy as np


fig = [23, 31, 32, 266]
SR = [0, 10, 20, 30, 40, 50]

#Assign tapers and bevels
bevelObj = "BalloonBevel"
taperObj = "BalloonTaper"
mkdir = "C:\\Users\\vayzenb\\Desktop\\Figure Generation\\"
imgdir = "Images\\"
rawDir = "SpatialRelation\\"

def takePic(objName, figNum):
	
	#Set file type
	bpy.context.scene.render.image_settings.file_format = "PNG"
	#Rotation coordinates
	picPlane = [0, 300, 90, 0]
	yRot = [0, -20, 30, 0]
	zRot = [[30, 60, 90], [-30, 0, 30], [30, 60, 90], [30, 60, 90]]
	
		#rotName = ["Front", "Top-Front", "Side-1", "Back", "Top-Back", "Side-2"]

	for kk in range(0, len(zRot)):
		
		picRot = [radians(picPlane[figNum]), radians(yRot[figNum]), radians(zRot[kk])]
		bpy.context.object.rotation_euler = picRot
		
		
		#Set file path for the render
		bpy.context.scene.render.filepath = mkdir + imgdir + objName + "_" + str(zRot[kk]) + ".png"
	
		#Take the picture
		bpy.ops.render.render(write_still = True)



#Read CSV
for ff in range(0, len(fig)):
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
		bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj]
		bpy.context.object.data.taper_object = bpy.data.objects[taperObj]
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

	    takePic("Figure_" + str(fig[ff]) + "_" + str(SR[xx]), ff)

	    finalObj.select = True
	    bpy.ops.wm.save_as_mainfile(filepath= mkdir + rawDir + "Figure_" + str(fig[ff]) + "_" + str(SR[xx] + ".blend") 
	    
	    bpy.ops.object.delete(use_global=False)
