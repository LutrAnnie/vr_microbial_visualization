# type: ignore
import bpy
from math import radians

def create_sun():
    print("Starting sun setup...")

    # --- 1. Delete existing sun lamps ---
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT' and obj.data.type == 'SUN':
            bpy.data.objects.remove(obj, do_unlink=True)    
            
    # --- 2. Create a new sun lamp ---
    bpy.ops.object.light_add(type='SUN', location=(-28.5, 20.7, 58.5))
    sun = bpy.context.active_object
    sun.name = "Sun"
    
    # --- 3. Settings ---
    sun.data.color = (0.347, 0.449, 1.0)
    sun.data.energy = 3.0  # Increase for brightness
    sun.data.angle = 0.009180432
    sun.rotation_mode = 'XYZ'
    sun.rotation_euler = (
        radians(-44.989),
        radians(19.359),
        radians(86.939)
    )   
    
    print("Sun created.")
