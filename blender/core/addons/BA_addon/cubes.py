import bpy

def create_fog_volume():
  """Places a cube around the scene as fog volume."""
  print("Creating fog volume.")
  
  # --- 1. Create the outer cube ---
  #bpy.ops.mesh.primitive_cube_add(location=(21, 21, 21))
  bpy.ops.mesh.primitive_cube_add(location=(7, 7, -7))
  fog_volume = bpy.context.active_object
  fog_volume.dimensions = (42, 42, 42) #type: ignore
  bpy.context.view_layer.objects.active = fog_volume
  #bpy.ops.object.transform_apply(scale= True)
  fog_volume.name = "FogVolume" #type: ignore 
  
  # --- 2. Create material ---
  fog_mat = bpy.data.materials.new(name="FogVolumeMaterial")
  fog_mat.use_nodes = True
  nodes = fog_mat.node_tree.nodes #type: ignore
  links = fog_mat.node_tree.links #type: ignore
  
  # --- 3. Clear default nodes ---
  for node in nodes:
    nodes.remove(node)
    
  # --- 4. Add principled volume shader node and output material node ---
  principled_volume = nodes.new("ShaderNodeVolumePrincipled")
  principled_volume.location = (0, 0)
  principled_volume.inputs["Color"].default_value = (0.5, 0.5, 0.5, 1.0) #type: ignore
  principled_volume.inputs["Density"].default_value = 0.05 #type: ignore
  
  output = nodes.new("ShaderNodeOutputMaterial")
  output.location = (300, 0)
  
  # --- 5. Link nodes ---
  links.new(principled_volume.outputs["Volume"], output.inputs["Volume"]) 
  
  # --- 6. Assign material ---
  fog_volume.data.materials.append(fog_mat) #type: ignore

  print("DONE.")
    