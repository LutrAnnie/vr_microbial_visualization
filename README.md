# Immersive Visualization of a Microscale Ecology Model 

This project focuses on building a pipeline to visualize data from a microscale ecology model in VR. 
It's focused specifically on phytoplankton and bacteria interactions in the ocean. 

## Project structure 

```
/home/path/to/project/
├── my_project/                									# main folder
│   ├──.vscode																	# json settings								
│   ├── blender/                								# scene and particles
|   |		├── .venv																# virtual environment Python 3.11.8 
│   │   ├── core/ 							                 		  
|   | 	|		├── addons/		
|   | 	|		|		├── BA_addon/ 	
|   | 	|		|		|		├── particles/
|   | 	|		|		|		|		├── blender_ops/
|   | 	|		|		|		|		|		├── __init__.py
|   | 	|		|		|		|		|		├── materials.py
|   | 	|		|		|		|		|		├── objects.py
|   | 	|		|		|		|		├── __init__.py
|   | 	|		|		|		|		├── constants.py
|   | 	|		|		|		|		├── load_all_data.py
|   | 	|		|		|		|		├── load_particles.py
|   | 	|		|		|		|		├── particle.py
|   | 	|		|		|		├── __init__.py
|   | 	|		|		|		├── blender_settings.py
|   | 	|		|		|		├── camera.py
|   | 	|		|		|		├── caustics_light.py
|   | 	|		|		|		├── cubes.py
|   | 	|		|		|		├── main.py
|   | 	|		|		|		├── sun_lamp.py
|   | 	|		├── caustics/												# bmp files for underwater effects
|   | 	|		├── data/														# put your data here
|   | 	|		├── resources/											# .blend file for DOM 
|   | 	|		├── scenes/													# you can save your .blend scenes here
|   | 	|		├── shell_scripts/									# bash scripts to rename grid and particle files
|   | 	|		|		├── rename_grid.sh
|   | 	|		|		├── rename_particle.sh
|   | 	|		├── example/
|   | 	|		|		├── data/												# 10 csv files as example for testing
|   | 	|		|   |   ├── grid/
|   | 	|		|   |   ├── particles/
|   | 	|		├── requirements_1.txt							# packages needed (in this venv)
|   ├── csv_to_openvdb/
|   |		├── .venv																# virtual environment Python 3.10.14  
|   |		├── csv_to_openvdb.py
|   |		├── requirements_2.txt									# packages needed (in this venv) 
|   ├──.gitignore 
│   └── README.md
│   └── vr_microbial_visualization.code-workspace
```

## Getting started

1. Create a folder my_project 
2. Install Blender 3.6.5 inside my_project (needed for vdb creation)
3. Download this git repo inside my_project folder
4. Install uv - used to download packages and create virtual environments (https://github.com/astral-sh/uv)

### Setting up PyOpenVDB

- Install PyOpenVDB directly to Blender 3.6.5
- anywhere in terminal run **either of the two** commands:

```bash
/path/to/blender/3.6/python/bin/python3.10 -m pip install pyopenvdb --target=/path/to/blender/3.6/python/lib/python3.10/site-packages
```
or
```bash
uv pip install pyopenvdb \
--target=/path/to/blender/blender/3.6/scripts/modules
```

**NOTE:** It might be better to use scripts/modules instead of site-packages

### Setting up Workspace
This pipeline uses two virtual environments running two Python versions. 

#### 1st Virtual Environment

- open project in VSCode (or other IDE but I haven't tested with another)
- open a terminal
- navigate to blender folder (inside my_project)
- set up the first virtual environment using Python 3.11.8
- run command in terminal:
```bash 
uv venv --python 3.11.8 .venv
```
- activate the virtual environment, run command in terminal:
```bash
source .venv/bin/activate
```
- install packages from txt file, run command in terminal:
```bash
uv pip install -r requirements_1.txt
```
- deactivate the virtual environment, run command in terminal:
```bash
deactivate
```

#### 2nd Virtual Environment

- using the terminal navigate to csv_to_openvdb folder
- set up the second virtual environment using Python 3.10.14
- run command in terminal:
```bash
uv venv --python 3.10.14 .venv
```
- activate the virtual environment, run command in terminal:
```bash
source .venv/bin/activate
```
- install packages from txt file, run command in terminal:
```bash
uv pip install -r requirements_2.txt
```

#### Blender

1. Install Blender version 5.0.1 or 5.1.0 (pipeline works for both versions)
2. Create a zip file from BA_addon folder
3. Open Blender 5.0.1+
4. Go to preferences and there to addons
5. Click "install addon from disk"
6. Search for the zip file you just created, Blender will open it
-> once installed you should see an addon named "Annies Tools" 
**NOTE:** if it doesn't work first go to extension tab and disable web search, then it will work

#### Environment Variable

- the scripts inside blender/ file must be run using a DAT_LOCATION environment variable
- to set it up open a terminal and run:
```bash
DATA_LOCATION=/home/path/to/my_project/blender/example/data/ blender
```
- this specifies the scripts used (found inside blender/ folder), the data used (found under folder example/data/), and the blender (in this case 5.1.0) 
- once you run the command via terminal it will open Blender

## Workflow

- The DATA_LOCATION command runs the main scripts 
- you will have to switch between environments with source activate and deactivate in VSCode to navigate between scripts in blender/ and the script in csv_to_openvdb/

### Gnerate vdb files and create DOM grid

1. in VSCode activate navigate to csv_to_openvdb folder and activate the environment
2. run:
```bash
 ~/path/to/my_project/blender-3.6.5/3.6/python/bin/python3.10 csv_to_openvdb.py
```
3. Open geonodes.blend file in resources/ folder 
4. paste the file path to the newly generated vdb files inside the .blend file 

### Run scripts in Blender

1. Open terminal
2. open blender using DATA_LOCATION
```bash
DATA_LOCATION=/home/path/to/my_project/blender/example/data/ blender
```
3. go to "Annies Tools" and click "Execute Main" (this will take a bit you can see what's happening in your terminal)

