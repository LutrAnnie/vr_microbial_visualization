from . import constants
import bmesh
import bpy

# --- 1. Check which files are seen for debugging ---
import os
print(os.listdir(os.path.dirname(__file__)))

"""
This script defines the Particle class.
"""

class Particle:
    # --- 2. Define attributes for Particle class ---
    COLOR = (1.0, 1.0, 1.0, 1.0)
    MESH = None
    # --- 3. Define methods for Particle class ---
    def __init__(self, particle_id,  x, y, z, lifecycle_stage, particle_radius:float) -> None:
        self.id: int = particle_id
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.lifecycle_stage: int = lifecycle_stage
        self.radius: float = particle_radius 
        # Storing time is useful for the animator: (time, x, y, z)
        self.keyframes: list[tuple[float, float, float, float]] = [] 
        self.alpha_keyframes: list[tuple[float, float]] = []

    def get_name(self) -> str:
        # Optional: Can override this in subclasses
        return f"particle-{self.id}"

    def add_keyframe(self, time, x, y, z):
        self.keyframes.append((time, x, y, z))
        
    @staticmethod
    def create_mesh():
        # --- 4. Create a single shared mesh ---
        # A. Add the sphere
        mesh = bpy.data.meshes.new("Particle_mesh")
        # B. Create geometry (fill the mesh) using bmesh
        bm = bmesh.new()
        bmesh.ops.create_icosphere(
            bm, 
            radius = 1.0, 
            subdivisions=3
        ) 
        bm.to_mesh(mesh)
        bm.free()
        
        return mesh
# --- 5. Define attributes for subclasses ---
class Oligo(Particle):
    
    COLOR = (0, 0.25, 1, 1) #blue
    MESH = Particle.create_mesh()

    
class Sphy(Particle):
    COLOR = (0, 1, 0.25, 1) #green
    MESH = Particle.create_mesh()

class Mphy(Particle):
    COLOR = (0, 1, 0, 1) #green
    MESH = Particle.create_mesh()
    
class Copio(Particle):
    COLOR = (1, 0, 0, 1) #red 
    MESH = Particle.create_mesh()

