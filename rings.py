import bpy
import math

def add_saturn_rings(parentobj, name, sizescale, imgname):
    """Add ring system for Saturn, in the planet's x-y-plane
    parentobj -- planet-object, to which the ring system is to be added as child
    name -- base name of the planet
    sizescale -- sizescale of the planet, to be used for rings as well
    img -- texture image for the rings
    """
    
    # add thin disk with hole inside; construct vertices and faces "by hand"
    rin = 68937 #km
    rout = 142731 #km
        
    rin *= sizescale
    rout *= sizescale
    
    bpy.ops.object.add(type='MESH', location = (0,0,0))
    ringobj = bpy.context.object
    ringobj.name = 'Planet-'+name+'-Rings'        
    mesh = ringobj.data
        
    verts = []
    verts2 = []
    num = 100
    for j in range(num):
        phi = j*1./num*(2*math.pi)
        x = rin*math.cos(phi)
        y = rin*math.sin(phi)
        z = 0             
        verts.append((x,y,z))
            
        phi = j*1./num*(2*math.pi)
        x = rout*math.cos(phi)
        y = rout*math.sin(phi)
        z = 0             
        verts2.append((x,y,z))

    verts = verts + verts2
    faces = []
    for j in range(num):
        j1 = j-1
        if j == 0: 
            j1 = num-1
        faces.append((j1,j,num+j, num+j1))
            
        
    mesh.from_pydata(verts, [], faces)
    mesh.update()
        
    # uv unwrap
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.follow_active_quads()
    bpy.ops.object.mode_set(mode='OBJECT')

    # create and add material
    matname = 'Material-'+name
    mat = bpy.data.materials.new(matname)
    mat.specular_intensity = 0.1
    mat.use_transparency = True
    mat.alpha = 0
    mat.specular_alpha = 0
    ringobj.data.materials.append(mat)

    # create texture, add image
    img = bpy.data.images.load(imgname)
    tex = bpy.data.textures.new(imgname, type='IMAGE')
    tex.image = img
    tex.use_flip_axis = True
    
    # add texture to material, set mapping
    mtex = mat.texture_slots.add()
    mtex.texture = tex

    mtex.texture_coords = 'UV'
    mtex.uv_layer = 'UVMap'
    mtex.mapping = 'FLAT'
    mtex.use_map_alpha = True
    
    # set the ring system's parent
    ringobj.parent = parentobj
        
    return ringobj


def add_uranus_rings(parentobj, name, sizescale):
    """ Add ring system for Uranus, in the planet's x-y-plane
    parentobj -- planet-object, to which the ring system is to be added as child
    name -- base name of the planet
    sizescale -- sizescale of the planet, to be used for rings as well
    """

    r = 51150 #km
    width = 60 #km
    # This is too small to be visible, so increase the ring size artificially.
    width *= 5

    r *= sizescale
    width *= sizescale
    
    ringname = 'Planet-'+name+'-Rings'

    # add circle for ring
    bpy.ops.curve.primitive_bezier_circle_add(radius=r, location=(0,0,0))
    ringobj = bpy.context.object
    ringobj.name = ringname


    # add bevel object for ring width
    bevelname = 'Planet-'+name+'-Rings-bevelobject'
    bpy.ops.curve.primitive_bezier_circle_add(radius=0.5*width, location=(0,0,0))
    bevelobj = bpy.context.object
    bevelobj.name = bevelname

    # set ring's thickness via bevel object
    ringobj.data.bevel_object = bevelobj
        
    # add material
    matname = 'Material-Rings-'+name
    mat = bpy.data.materials.new(matname)
    mat.specular_intensity = 0.1
    mat.diffuse_color = [0.8,0.8,1.0]
    mat.diffuse_intensity = 1.0
    mat.emit = 0.1
    ringobj.data.materials.append(mat)

    # set parent        
    ringobj.parent = parentobj

    return ringobj

