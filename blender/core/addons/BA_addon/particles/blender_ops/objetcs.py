import bpy
import bmesh
from mathutils import Vector

from .materials import get_or_create_material
from ..particle import Particle

def clear_particles(clear_animation=True, clear_materials=False, remove_objects=False)->None:
  """ Clear animation data, materials or remove objects
  Arguments: 
  clear_animation: bool - remove animation yes or no?
  clear_materials: bool - remove materials yes or no?
  remove_objects: bool - remove objects yes or no? 
  """   
  for obj in list(bpy.data.objects):
    if not obj.name.startswith("particle"):
      continue
    
    # --- 1. Clear animation data ---
    if clear_animation and obj.animation_data is not None:
      bpy.data.actions.remove(obj.animation_data.action) # type: ignore
      obj.animation_data_clear()
    
    # --- 2. Clear materials ---
    if clear_materials:
      for slot in obj.material_slots:
        mat = slot.material
        if mat:
          bpy.data.materials.remove(mat)
            
    # --- 3. Remove objects --- 
    if remove_objects:
      bpy.data.objects.remove(obj, do_unlink=True)
      

def create_sphere(name: str, particle: Particle)->object: 
  """
  Blender functions to create the spheres. 
  
  :param name: Particle id
  :type name: str
  :param particle: Particle object
  :type particle: Particle
  :return: Particle sphere object
  :rtype: object
  """
  # --- 1. Get starting location and shared material from cache --- 
  coordinates = Vector((particle.x, particle.y, particle.z))
  mat = get_or_create_material(particle)

  # --- 2. Link mesh ---
  obj = bpy.data.objects.new(name, particle.MESH)
  bpy.context.collection.objects.link(obj)
  
  # --- 3. Link material ---
  obj.active_material = mat
  obj.material_slots[0].link = "OBJECT"
  obj.active_material = mat # THIS IS IMPORTANT! KEEP!
  obj.location = coordinates
  obj.scale = particle.radius, particle.radius, particle.radius 
  
  # --- 4. Smooth and subdivide ---
  for face in obj.data.polygons: # type: ignore
    face.use_smooth = True
  
  # --- 5. Create a tiling modifier for each particle ---
  ### UNCOMMENT THIS FOR TILING VERSION #####
  #for axis in range(3):
  #  array = obj.modifiers.new("Array", type="ARRAY")
  #  array.count = 3 #type: ignore
  #  array.use_relative_offset = False # type: ignore
  #  array.use_constant_offset = True #type: ignore
  #  array.constant_offset_displace[0] = 0 # type: ignore 
  #  array.constant_offset_displace[axis] = 14 / particle.radius #type: ignore 
  
  print(f"Creating new particle: {name} at {coordinates}")
  
  return obj


def sphere_visibility(obj, p, FPS)->None:
  first_frame = p.keyframes[0][0] * FPS
  last_frame  = p.keyframes[-1][0] * FPS
  
  # Hide before it appears
  obj.hide_render = True
  obj.hide_viewport = True
  obj.keyframe_insert("hide_render", frame=first_frame - 1)
  obj.keyframe_insert("hide_viewport", frame=first_frame - 1)

  # Show when it starts
  obj.hide_render = False
  obj.hide_viewport = False
  obj.keyframe_insert("hide_render", frame=first_frame)
  obj.keyframe_insert("hide_viewport", frame=first_frame)

  # Hide after it disappears
  obj.hide_render = True
  obj.hide_viewport = True
  obj.keyframe_insert("hide_render", frame=last_frame + 1)
  obj.keyframe_insert("hide_viewport", frame=last_frame + 1)
