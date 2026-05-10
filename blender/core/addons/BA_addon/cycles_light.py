# type: ignore
import bpy
import pathlib
import os
import glob

def create_cycles_light():
  """Generates a spot light containing caustics - use with cycles"""
  
  # --- 1. Make sure existing spot lights are deleted first ---
  for obj in bpy.data.objects:
    if obj.type == 'LIGHT' and obj.data.type == 'SPOT': #type: ignore
      bpy.data.objects.remove(obj, do_unlink=True)
      
  # --- 2. Create spot light: ---
  bpy.ops.object.light_add(type="SPOT", location=(21, 21, 60)) #TODO: position good? 
  spot = bpy.context.active_object
  spot.name = "Cycles_Light" # type: ignore
  
  # A. Provide general settings
  spot.data.energy = 9999 # type: ignore
  spot.data.color = (0.496, 0.971, 1) # type: ignore
  spot.data.spot_size = 1.2269665 
  spot.data.use_shadow # type: ignore
  
  # --- 3. Create the caustics light texture ---
  
  # A. Create nodes
  spot.data.use_nodes = True 
  nodes = spot.data.node_tree.nodes
  
  texture_coordinate = nodes.new(type="ShaderNodeTexCoord")
  mapping = nodes.new(type="ShaderNodeMapping")
  caustics = nodes.new(type="ShaderNodeTexImage")
  color_ramp = nodes.new(type="ShaderNodeValToRGB")
  emission = nodes.get('Emission')
  output = nodes.get('Light Output')
  
  # B. Create node layout 
  texture_coordinate.location = (-800, 0)
  mapping.location = (-600, 0)
  caustics.location = (-400, 0)
  color_ramp.location = (0, 0)
  emission.location = (400, 0)
  output.location = (600, 0)
  
  # C. Load image sequence to image texture node
  # Build path to images
  DATA_LOCATION = os.environ['DATA_LOCATION']
  caustic_dir = pathlib.Path(DATA_LOCATION).parent.parent/"core"/"caustics"
  
  # Create an image sequence 
  bmp_files = sorted(caustic_dir.glob("*.bmp"))
  if not bmp_files:
    raise RuntimeError("No BMP Images found in caustics directory")
  
  img = bpy.data.images.load(str(bmp_files[0]))
  img.source = 'SEQUENCE'
  caustics.image = img
  caustics.image_user.use_auto_refresh = True
  caustics.image_user.use_cyclic = True
  caustics.image_user.frame_duration = len(bmp_files)

  # D. Set color ramp values #TODO: do I need this? 
  
  # E. Link nodes in correct order
  links = spot.data.node_tree.links
  # texture coordinate -> mapping
  links.new(texture_coordinate.outputs["UV"], mapping.inputs["Vector"])
  # mapping -> caustics
  links.new(mapping.outputs["Vector"], caustics.inputs["Vector"])
  # caustics -> color ramp
  links.new(caustics.outputs["Color"], color_ramp.inputs["Fac"])
  # color ramp -> emission 
  links.new(color_ramp.outputs["Color"], emission.inputs["Color"])
  # emission -> light output
  # this is already default in blender 