import bpy
import sys
import importlib

# --- 1. Title and category of blender add-on ---
bl_info = {
  "name": "My blender BA thesis scripts",
  "blender": (3, 6, 5),
  "category": "Development"
}

# --- 2. Create button panel ---
# A. Loaded script
def register():
  print("Script loaded.")
  bpy.utils.register_class(_PT_ButtonPanel)
  bpy.utils.register_class(MainButton)
  bpy.utils.register_class(ReloadButton)

# B. Unloaded script
def unregister():
  print("Script unloaded.")
  bpy.utils.unregister_class(_PT_ButtonPanel)
  bpy.utils.unregister_class(MainButton)
  bpy.utils.unregister_class(ReloadButton)

# C. Create main button - on press execute main script
class MainButton(bpy.types.Operator):
  bl_idname = "main.button"
  bl_label = "Execute Main"
  
  def execute(self, context): # type: ignore 
    from .main import main 
    main()
    return {"FINISHED"}

# D. Create reload button - on press reload scripts
class ReloadButton(bpy.types.Operator):
    bl_idname = "reload.button"
    bl_label = "Reload"

    def execute(self, context): # type: ignore
        my_modules: list[str] = []
        for mod_name in sys.modules:
            if not mod_name.startswith("annieBA"):
                continue
            my_modules.append(mod_name)
        for mod_name in my_modules:
            print(f"Reloading {mod_name}")
            importlib.reload(sys.modules[mod_name])
        bpy.ops.script.reload()
        return {"FINISHED"}

# --- 3. Panel config ---
class _PT_ButtonPanel(bpy.types.Panel):
  bl_label = "annies tolle ba tools"
  bl_idname = "VIEW_PT_buttonpanel"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_category = "Annies Tools"
  
  def draw(self, context):
    layout = self.layout
    layout.operator("main.button", icon = "DISCLOSURE_TRI_RIGHT")
    layout.operator("reload.button", icon = "FILE_REFRESH")
    