import bpy
import pathlib
import os
import glob

def create_spot_light():
  """Generates a spot light above the water plane"""
  print("Creating spot light and water plane.")
  
  # --- 1. Make sure existing spot lights are deleted first ---
  for obj in bpy.data.objects:
    if(
      obj.type == 'LIGHT' 
      and obj.data.type == 'SPOT' #type: ignore
      and obj.name != 'Cycles_Light'
    ): 
      bpy.data.objects.remove(obj, do_unlink=True)
      
  # --- 2. Create spot light ---
  #versuch: z 76
  #bpy.ops.object.light_add(type="SPOT", location=(21, 21, 90)) 
  #bpy.ops.object.light_add(type="SPOT", location=(21, 21, 76)) 
  bpy.ops.object.light_add(type="SPOT", location=(8.0007, 8.0869, 26.94)) 
  spot = bpy.context.active_object
  spot.name = "Spot_Light" # type: ignore
  
  # A. Provide general settings
  spot.data.energy = 10000000 # type: ignore
  spot.data.color = (0.506, 0.737, 1) # type: ignore
  spot.data.spot_size = 1.0471976 #type: ignore
  spot.data.use_shadow # type: ignore
  
def create_water_plane():
  """Creates a plane with caustics texture above the cube"""
  
  # --- 1. Add a plane ---
  #bpy.ops.mesh.primitive_plane_add(location=(22.2, 19.5, 51))
  bpy.ops.mesh.primitive_plane_add(location=(7, 7, 15))
  plane = bpy.context.active_object
  #plane.scale = (21, 21, 1) #type: ignore
  plane.dimensions = (18.3, 18.3, 0) #type: ignore
  plane.name = "WaterPlane" #type: ignore

  # --- 2. Settings for texture based transparency ---
  mat = bpy.data.materials.new("CausticsMat")
  mat.use_nodes = True
  mat.blend_method = 'BLEND'
  mat.use_transparent_shadow = True #Optional if I want transparent shadows
  mat.use_backface_culling = True #optional: helps avoid glitches
  
  # --- 3. Create material using nodes ---
  tree = mat.node_tree
  nodes = tree.nodes #type: ignore
  links = tree.links # type: ignore

  nodes.clear()
  
  # --- 4. Add nodes ---
  texture_coordinate = nodes.new(type="ShaderNodeTexCoord")
  mapping = nodes.new(type="ShaderNodeMapping")
  caustics = nodes.new(type="ShaderNodeTexImage")
  transparent = nodes.new("ShaderNodeBsdfTransparent")
  output = nodes.new("ShaderNodeOutputMaterial")

  # A. Set layout
  texture_coordinate.location = (-400, 0)
  mapping.location = (-200, 0)
  caustics.location = (0, 0)
  transparent.location = (200, 0)
  output.location = (400, 0)
  
  # B. Load image sequence to image texture node
  # Build path to images
  DATA_LOCATION = os.environ['DATA_LOCATION']
  caustic_dir = pathlib.Path(DATA_LOCATION).parent.parent/"core"/"caustics"
  
  # Create an image sequence 
  bmp_files = sorted(caustic_dir.glob("*.bmp"))
  if not bmp_files:
    raise RuntimeError("No BMP Images found in caustics directory")
  
  img = bpy.data.images.load(str(bmp_files[0]))
  img.source = 'SEQUENCE'
  caustics.image = img #type: ignore
  caustics.image_user.use_auto_refresh = True #type: ignore
  caustics.image_user.use_cyclic = True #type: ignore
  caustics.image_user.frame_duration = len(bmp_files) #type: ignore
  
  # C. Link nodes in correct order
  # links = plane.data.node_tree.links #type: ignore
  
  # texture coordinate -> mapping
  links.new(texture_coordinate.outputs["UV"], mapping.inputs["Vector"])
  # mapping -> caustics
  links.new(mapping.outputs["Vector"], caustics.inputs["Vector"])
  # caustics -> transparent
  links.new(caustics.outputs["Color"], transparent.inputs["Color"])
  # transparent -> output material 
  links.new(transparent.outputs["BSDF"], output.inputs["Surface"])

  plane.data.materials.append(mat) #type: ignore

  print("Spot light and water plane created.")
  
  
  #TODO: add color ramp to waterplane pos 0: 0, pos 1: 0.595