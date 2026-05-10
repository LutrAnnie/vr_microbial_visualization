#for debugging
import bpy
from ..particle import Particle
from ..load_all_data import STAGE_TO_ALPHA

# --- 1. Create dictionary ---
material_cache = {}

def get_or_create_material(particle: Particle):
    """
    Sphere material set up. 
    """
    # --- 2. Define key: Type, lifecycle stage ---
    key = particle.__class__.__name__, particle.lifecycle_stage 
    
    if key in material_cache:
        return material_cache[key]
    
    # --- 3. Create material ---
    mat = bpy.data.materials.new(name=f"Material_{particle.__class__.__name__}_{particle.lifecycle_stage}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND' #enables transparency 
    mat.use_transparent_shadow = True #Optional if I want transparent shadows
    mat.use_backface_culling = True #helps avoid glitches
    
    # A. Set up nodes
    nodes = mat.node_tree.nodes # type: ignore
    nodes.clear()

    # B. Create nodes    
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    
    mat.node_tree.links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"]) # type: ignore
    
    # C. Settings
    bsdf.inputs["Base Color"].default_value = particle.COLOR # type: ignore
    bsdf.inputs["Alpha"].default_value = STAGE_TO_ALPHA[particle.lifecycle_stage] # initial value # type: ignore
    bsdf.inputs["Specular IOR Level"].default_value = 0.3 #shininess of surface in terms of reflected highlights # type: ignore
    bsdf.inputs["Roughness"].default_value = 0.5 #matte or mirror-like surface --> try 0.3 for more jelly-like structure # type: ignore
    
    material_cache[key] = mat
    return mat  