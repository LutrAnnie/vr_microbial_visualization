import bpy
import os
import sys
import pathlib

# --- 1. Importing scripts using relative import ---
# A. Import settings
from .blender_settings import apply_blender_settings

# B. Import particles
from .particles.load_particles import load_particles

# C. Import lights
from .sun_lamp import create_sun
from .cycles_light import create_cycles_light
from .caustics_light import create_spot_light, create_water_plane

# D. Import volume shader
from .cubes import create_fog_volume

# E. Import VR camera
from .camera import create_camera_VR


def main():
  """
  The main script loads all other scripts and executes them.
  """
  print("Starting Blender automation script...")
  
  # --- 2. Define location of stored data ---
  
  # /home/lutra/Documents/BA/lutra_project/blender/example/data/
  # DATA_LOCATION=/home/lutra/Documents/BA/lutra_project/blender/example/data/ blender
  DATA_LOCATION = os.environ['DATA_LOCATION']
  print(DATA_LOCATION)
  BLEND_LOCATION = pathlib.Path(DATA_LOCATION).parent.parent/"core"/"resources"/"geonodes_portal_27-03-26.blend"
  
  apply_blender_settings()
  
  # --- 3. Import the grid volume ---
  bpy.ops.wm.append(
    directory=str(BLEND_LOCATION / "Collection") + "/",
    filename="SimulationRender"
  )
  
  # --- 4. Execute scripts --- 
  load_particles()

  create_sun()
  
  create_fog_volume()
  
  create_cycles_light()
  
  create_spot_light()
  
  create_water_plane()
  
  create_camera_VR()
  
  print("DONE.")
  print(DATA_LOCATION)
  
if __name__ == "__main__":
  main()