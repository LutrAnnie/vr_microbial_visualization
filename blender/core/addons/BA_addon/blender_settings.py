import bpy
import os

def apply_blender_settings():
    """
    This script stores general information for Blender.
    """

    print("Starting blender settings setup...")

    # --- 1. Clear scene ---
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- 2. Set render engine to Cycles or Eevee (stereo works in both) ---
    # Default: EEVEE
    bpy.data.scenes["Scene"].render.engine = 'BLENDER_EEVEE' #type: ignore
    
    ###### For caustics and lighting use CYCLES #######
    #bpy.data.scenes["Scene"].render.engine = 'CYCLES' #type: ignore
    #bpy.data.scenes["Scene"].cycles.device = 'GPU'
    
    # --- 3. Set resolution ---
    bpy.context.scene.render.resolution_x = 7680
    bpy.context.scene.render.resolution_y = 7680  
    bpy.data.scenes["Scene"].render.resolution_percentage = 25
    
    # --- 4. Set render file format ---
    bpy.context.scene.render.image_settings.file_format = 'TIFF'
    
    # --- 5. Set FPS to 90 FPS ---
    bpy.context.scene.render.fps = 90

    # --- 6. Ensure world and tree node exist ---
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    nt = world.node_tree
    nodes = nt.nodes # type: ignore
    
    for n in nodes:
        nodes.remove(n)

    # --- 7. Get or create background node ---
    bg = nodes.get("Background")
    if not bg:
        bg = nodes.new(type="ShaderNodeBackground")
        bg.name = "Background"
        bg.location = (0, 0)
    # Set background color
    bg.inputs[0].default_value = (0, 0, 0, 1) # type: ignore
    
    # --- 8. Get DATA_LOCATION from environment ---
    try:
        DATA_LOCATION = os.environ['DATA_LOCATION']
    except KeyError:
        raise RuntimeError("DATA_LOCATION environment variable not set.")
    
    #TODO: set this for renderings
    #output path needs to be adjusted once needed
    #output_path = bpy.context.scene.render.filepath = DATA_LOCATION + "/../../output/test_3/"
    #bpy.context.scene.render.filepath = output_path + "test3_ORTHO_30-05-25"

    print("Blender settings configured.")

#apply_blender_settings()

