# Microbial Scene VR Visualization (Bachelor Thesis)

This project is a Blender + Godot workflow to visualize microbial scenes in VR. 
Its focused specifically on phytoplankton and bacteria interactions within the ocean. 

## 🔧 Project structure 

```
/home/lutra/Documents/BA/
├── lutra_project/                	# Main folder
│   ├──.venv												#virtual environment
│   ├──.vscode											#json settings inside
│   ├──BA_Felisiak									#example for Falk
│   ├── blender/                  	
│   │   ├── example/                  		  
|   | 	├── core/		  	
|   |   ├── data/             	# CSVs or data files 
│   │   |   ├── scenes/               	
│   │   |   |── scripts/              	   
|   |   |   |   ├── camera/
|   |   |   |   ├── grid/
|   |   |   |   ├── particles/
|   |   |   |   ├── blender-settings.py  
|   |   |   |   ├──sun-lamp.py
|   |   |   |   ├──.gitignore 
|   |   |   |   ├──main.py
|   |   |   |   ├──__init__.py
│   ├── godot_projects/                    	# Godot project folder
|   |   ├── example_project/
|   |   ├── core_project/  
│   │   |    ├── assets/		# Imported Blender models, textures, etc.
│   │   │    |   ├── models/			
│   │   │    |   ├── textures/
│   │   |    ├── scenes/		# Godot scenes for the VR environment
│   │   │    |   ├── main_scene.tscn
│   │   │    |   └── tests/
│   │   |    ├── blueprints/
│   │   |    ├── scripts/		# GDScripts controlling scene behavior
│   │   |    └── project.godot
│   └── README.md
```

## 🧬 Workflow

1. **Blender**:
	- Scene creation using python and CSV data
	- Export .blend files for import into Godot
	
2. **Godot**:
	- Import scenes for realtime rendering
	- Use for VR viewing, navigation, and interaction 
	
## ✅ Current Status 

- [X] Example Blender scenes created (from Mats project)
- [X] Updated particles sript - share mesh and share color cache
- [X] Wrote VR camera script
- [X] particles don't emmit light sun lamp does
- [X] shared script for windows

## 🗂 Notes

- Only clean .blend files are kept in scenes/
- Use scripts/ for all Pyhton or GDScripts 
- VR support will be handled later using OpenXR
- The example/ folders are only for learning/testing - not part of the final pipeline

## Naming convention
[project]_[feature-or-change]_[camera/scene/view]_[DD-MM-YYYY]_[vX].blend

--> phytoscene_matcache_PANO_11-06-2025_v1.blend

## 📍 Next Steps

- [ ] Understand blender and particles
- [ ] Test with different data
- [X] Workflow setup with VS Code and Blender
