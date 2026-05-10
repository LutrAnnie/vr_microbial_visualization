import bpy
import os
import bmesh

# --- 1. Import new data loader script ---
from .load_all_data import (
    load_all_data, 
    adjust_copio_paths, 
    create_particle_objects,
    RAW_BOX_SIZE,
    COORD_SCALE,
    check_particle_lifetimes,
)

from .blender_ops.objetcs import sphere_visibility

def load_particles():
    """
    Load, clean particle data. Map data to particles.
    Create particle meshes. 
    """
    # --- 2. Import scripts for blender objects ---
    from .blender_ops.objetcs import create_sphere, clear_particles
    
    # A. Clear existing scene
    clear_particles(clear_animation=True, clear_materials=True, remove_objects=True)

    # --- 3. LOAD & PROCESS DATA ---
    print("Loading and processing data...")
    
    # A. Get Raw Data (DataFrame)
    #raw_df = load_all_data(data_dir=os.environ['DATA_LOCATION'] + "/particles") 
    raw_df = load_all_data(data_dir="/home/lutra/Documents/BA/data_1000/particle")
    

    # B. Fix Physics (DataFrame -> DataFrame)
    clean_df = adjust_copio_paths(raw_df)
    
    
    # C. Create Objects (DataFrame -> List of Particle Classes)
    # NOW there's the list of objects I can iterate over
    all_particles = create_particle_objects(clean_df)
    
    # D. Create base particle collection
    col_name = "Particle_Base"
    particles_col = bpy.data.collections.get(col_name)
    if particles_col is None:
        particles_col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(particles_col)

    # --- 4. Create the objects in blender ---
    FPS = 90
    print(f"Baking {len(all_particles)} particles into Blender...")

    for p in all_particles:
        # A. Create the Mesh
        obj_name = p.get_name()
        obj: bpy.types.Object = create_sphere(obj_name, p)  #type: ignore
        
        # B. Move object into particle collection
        particles_col.objects.link(obj)
        for col in obj.users_collection:
            if col != particles_col:
                col.objects.unlink(obj)
                
        # C. Create animation
        for time_step, x, y, z in p.keyframes:
            obj.location = (x, y, z)
            frame_num = time_step * FPS 
            obj.keyframe_insert(data_path="location", frame=frame_num)
            
        # D. Toggle visbility of spheres 
        toggle_visibility = sphere_visibility(obj, p, FPS=90)
        

    # --- 5. Set scene timeline ---
    # A. Find maximum time step
    if all_particles and any(p.keyframes for p in all_particles):
        max_time_step = max(
            time_step
            for p in all_particles
            for time_step, _, _, _ in p.keyframes
        )
    else: max_time_step = 0
    
    ### DEBUGGING ### 
    print("Particles in list:", len(all_particles))
    print("Particle objects in scene:",
        len([obj for obj in bpy.data.objects if obj.name.startswith("particle")]))
    
    check_exist = check_particle_lifetimes(clean_df)
    
    # B. Set start and end time
    scene = bpy.context.scene
    scene.frame_start = 90 
    scene.frame_end = (max_time_step * FPS) - 1 
    scene.frame_current = scene.frame_end

    print("Done! Animation ready.")






