import bpy
from math import radians

def create_camera_VR():
  """
  Place a camera in the scene with settings
  suitable for VR.
  Notice: VR settings only work in cycles.
  """
  
  # --- 1. Delete existing camera objetcs ---
  for obj in bpy.data.objects:
    if obj.name.startswith("Camera"):
        if obj.animation_data is not None:
            bpy.data.actions.remove(obj.animation_data.action) #type: ignore
            obj.animation_data_clear()
        bpy.data.objects.remove(obj, do_unlink=True)

  # --- 2. Create camera ---
  camera_data = bpy.data.cameras.new(name="CameraVR")
  camera_object = bpy.data.objects.new("CameraVR", camera_data)
  bpy.context.collection.objects.link(camera_object)
  bpy.context.scene.camera = camera_object

  # --- 3. General Settings ---
  camera = bpy.data.objects["CameraVR"]
  #camera.location = (21, 21, 21)
  camera.location = (7, 7, 7)
  camera.rotation_mode = 'XYZ'
  camera.rotation_euler = (
      radians(73.539),
      radians(-0.000003),
      radians(-157.04)
    ) 
  
  # --- 4. VR Settings ---
  # A. Lens type panoramic and equirectangular
  camera.data.type = 'PANO' #type: ignore
  camera.data.panorama_type = 'EQUIRECTANGULAR' #type: ignore
  
  # B. Use sperical mode 
  bpy.context.scene.camera.data.stereo.convergence_mode = 'PARALLEL' #type: ignore
  bpy.context.scene.render.use_multiview = True
  
  # C. Enable steroscopic
  bpy.context.scene.render.image_settings.views_format = 'STEREO_3D'
  
  # D. Change stereo mode 
  bpy.context.scene.render.image_settings.stereo_3d_format.display_mode = 'TOPBOTTOM'
  bpy.context.scene.render.image_settings.stereo_3d_format.use_squeezed_frame = True
  bpy.data.cameras["CameraVR"].stereo.use_spherical_stereo = True 
  