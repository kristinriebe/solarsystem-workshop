import bpy
import os
import csv
import math

# This file is a template for the workshop on 
# creating planets in Blender. Adjust, rewrite and 
# extend the functions according to your own needs.

def delete_planets():
    """Delete objects with names matching 'Planet-*'"""
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Planet-*")
    n = len(bpy.context.selected_objects)
    bpy.ops.object.delete()

    print("%d planet(s) were deleted." % n)

    return


def delete_unused_materials():
    """Delete all unused materials (also done automatically after reload)"""
    i = 0
    for mat in bpy.data.materials:
        if mat.users == 0:
            name = mat.name
            bpy.data.materials.remove(mat)
            i = i + 1
            print("Deleted material ", name)

    print("%d materials were deleted." % i)

    return


def delete_unused_textures():
    """Delete all unused textures"""
    # Be careful, since this really deletes all textures which are currently 
    # not used. It may thus delete more than you intended.
    i = 0
    for tex in bpy.data.textures:
        if tex.users == 0:
            name = tex.name
            bpy.data.textures.remove(tex)
            i = i + 1
            print("Deleted texture ", name)
            
    print("%d textures were deleted." % i)
    
    return


def add_texture(mat, imgname):
    """Add image texture to given material, map as sphere
    mat -- material
    imgname -- name of texture image file
    """
    
    # create texture, add image
    img = bpy.data.images.load(imgname)
    tex = bpy.data.textures.new(imgname, type='IMAGE')
    tex.image = img
    
    # add texture to material, set mapping
    mtex = mat.texture_slots.add()
    mtex.texture = tex
    mtex.texture_coords = 'ORCO'
    mtex.mapping = 'SPHERE' 

    return


def add_material(obj, name):
    """Add material to an object
    obj -- object to which the material is appended
    name -- basename to be added to material name
    """
    
    # create a material
    matname = "Material-" + name
    mat = bpy.data.materials.new(matname)
    mat.diffuse_color = [0,0,1]
    mat.specular_intensity = 0.1

    # add material to the object
    obj.data.materials.append(mat)

    return mat


def add_sphere(name, location):
    """Add smooth sphere to current scene at given location
    name -- name for new sphere
    location -- location for the new sphere
    """
    
    # add object
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48, ring_count=24, size=1.0,
        location=location, rotation=[0,0,0])
    
    # get object
    obj = bpy.context.object
    
    # set name and smooth shading
    obj.name = name
    bpy.ops.object.shade_smooth()
       
    print("Sphere '%s' created." % name)
   
    return obj
 

if __name__ == '__main__':

    # set current directory, in case we need it to load files
    dir = os.path.dirname(bpy.data.filepath) + os.sep

    # delete objects that were previously created by this script
    delete_planets()
    # also delete unused materials and textures
    delete_unused_materials()
    delete_unused_textures()
    
    # This would be a good place to start a loop over all planets.
    
    location = [2.5,0,0]

    name = "Earth"
    objname = "Planet-" + name

    # create planet as sphere object
    obj = add_sphere(objname, location)
    
    # add a material to the object
    mat = add_material(obj, name)
    
    # add texture to the material
    #imgname = dir + "textures/earth.jpg"
    #add_texture(mat, imgname)

    # add flattening of planet-sphere
    
    # add axial tilt

    # add orbit paths
    
    # add orbit animation
    
    # add rotation animation
    
    # add rings for some planets
        
    # end of loop
