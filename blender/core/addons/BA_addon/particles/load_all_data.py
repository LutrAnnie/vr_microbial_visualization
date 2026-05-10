import glob
import os
import re

import numpy as np
import pandas as pd

from .particle import Copio, Mphy, Sphy, Oligo
try:
    from . import constants #type: ignore
except ImportError:
    # Fallback for running this script standalone
    class constants:
        COPIO = 1
        OLIGO = 2
        SPHY = 3
        MPHY = 4
        HEALTHY = [1, 2]
        SENESCENT = 3
        DEAD = 4

# --- CONSTANTS ---
RAW_BOX_SIZE = (1400.0, 1400.0, 1400.0)
COORD_SCALE = 0.01

COLUMNS = [
    "row_id", "particle_id", "species_id", "lifecycle_stage",
    "x", "y", "z", "theta", "phi", "radius",
]

USE_COLS = ["particle_id", "species_id", "lifecycle_stage", "x", "y", "z", "radius"]


# --- 1. MAP LIFECYCLE-STAGE TO ALPHA VALUE ---

STAGE_TO_ALPHA = {
    constants.HEALTHY[0]: 1.0,
    constants.HEALTHY[1]: 1.0,
    constants.SENESCENT: 0.6, #old 0.4
    constants.DEAD: 0.4, #old 0.1
}

# --- 2. DATA LOADING & PROCESSING ---

def load_all_data(data_dir="data/"):
    """
    Load all data once and then process globally.
    """
    #print("Looking in:", data_dir)
    #print("Exists?", os.path.exists(data_dir))
    #print("Files:", os.listdir(data_dir) if os.path.exists(data_dir) else "DIR NOT FOUND")

    all_frames = []
    # --- 1. Find all csv files and sort them ---
    files = glob.glob(os.path.join(data_dir, "particle-*.csv"))
    # A. Sort numerically by the number in the filename
    files.sort(key=lambda f: int(re.search(r"(\d+)", f).group())) #type: ignore

    print(f"Loading {len(files)} files...")

    # --- 2. Loop over sorted files --- 
    for time_step, file_path in enumerate(files):
        # A. Read csv file into pandas dataframe 
        #df = pd.read_csv(file_path, names=COLUMNS, header=None, usecols=COLUMNS)
        
        df = pd.read_csv(
            file_path,
            sep=r"\s+|,",
            engine="python",
            header=None
        ).dropna(axis=1, how="all")
    
        df.columns = COLUMNS
        df = df[USE_COLS]
        
        # B. Add timestep column
        df["time"] = time_step + 1
        # C. Filtered list
        all_frames.append(df[USE_COLS + ["time"]])

    # --- 3. Combine dataframes and return it --- 
    full_data = pd.concat(all_frames, ignore_index=True)
    full_data["particle_id"] = full_data["particle_id"].astype(int)
    return full_data.sort_values(by=["particle_id", "time"])


def adjust_copio_paths(df):
    """
    Correct Copio positions to sit on the rim of partner.
    """
    print("Adjusting Copio positions to outer rim...")
    
    # --- 1. Get correct species ---
    copios = df[df["species_id"] == constants.COPIO].copy()
    targets = df[df["species_id"].isin([constants.MPHY, constants.SPHY])].copy()

    # Include Copio's radius in the merge (renamed to avoid collision)
    # --- 2. Merge dataframe to use only relevant arguments ---
    overlaps = pd.merge(
        copios[["particle_id", "time", "x", "y", "z", "radius"]].rename(columns={"radius": "radius_copio"}),
        targets[["time", "x", "y", "z", "radius"]].rename(columns={"radius": "radius_partner"}),
        on=["time", "x", "y", "z"],
        how="inner"
    )

    if overlaps.empty:
        return df

    # --- 3. Generate stable random vectors ---
    unique_ids = overlaps["particle_id"].unique()
    rng = np.random.default_rng(seed=42) 
    vecs = rng.normal(size=(len(unique_ids), 3))
    vecs /= np.linalg.norm(vecs, axis=1)[:, np.newaxis]
    
    vec_map = pd.DataFrame(vecs, columns=["vx", "vy", "vz"])
    vec_map["particle_id"] = unique_ids
    overlaps = overlaps.merge(vec_map, on="particle_id")

    # Apply offsets: position Copio center at (radius_partner + radius_copio) from partner center
    # This places the Copio just outside, touching the partner's surface
    # SCALE CORRECTION: Radii use RADIUS_SCALE=0.1 but coords use COORD_SCALE=0.01
    # multiply by (RADIUS_SCALE / COORD_SCALE) = 10 to match scales
    
    # --- 4. Apply offsets and scaling ---
    scale_correction = 10.0  # = 0.1 / 0.01
    total_offset = (overlaps["radius_partner"] + overlaps["radius_copio"]) * scale_correction
    overlaps["dx"] = overlaps["vx"] * total_offset
    overlaps["dy"] = overlaps["vy"] * total_offset
    overlaps["dz"] = overlaps["vz"] * total_offset

    #--- 5. Update Dataframe ---
    adjustments = overlaps.set_index(["particle_id", "time"])[["dx", "dy", "dz"]]
    df = df.set_index(["particle_id", "time"])
    common = df.index.intersection(adjustments.index)
    
    if not common.empty:
        df.loc[common, "x"] += adjustments.loc[common, "dx"]
        df.loc[common, "y"] += adjustments.loc[common, "dy"]
        df.loc[common, "z"] += adjustments.loc[common, "dz"]

    return df.reset_index()


def create_particle_objects(clean_df):
    """
    Convert Dataframe groups into specific Python objects.
    """
    print("Creating particle objects...")
    particles = []
    
    # --- 1. Pre-scale for Blender (0.01) ---
    scale = COORD_SCALE 
    radius_scale = 0.1

    # --- 2. Loop over particles --- 
    for p_id, group in clean_df.groupby("particle_id"):
        # A. Get inforamtion from the first frame
        first = group.iloc[0]
        s_id = int(first["species_id"])
        rad = float(first["radius"]) * radius_scale
        stage = int(first["lifecycle_stage"])
        
        # B. Get initial position (scaled)
        x, y, z = first["x"]*scale, first["y"]*scale, first["z"]*scale

        # --- 3. Factory logic: match particle subclass to p ---
        p = None
        if s_id == constants.COPIO:
            p = Copio(p_id, x, y, z, stage, rad)
        elif s_id == constants.OLIGO:
            p = Oligo(p_id, x, y, z, stage, rad)
        elif s_id == constants.SPHY:
            p = Sphy(p_id, x, y, z, stage, rad)
        elif s_id == constants.MPHY:
            p = Mphy(p_id, x, y, z, stage, rad)
        else:
            continue # Skip unknown
            #raise ValueError(f"Unexpected species_id: {species_id}")

        # --- 4. Populate Keyframes ---
        # A. Convert numpy arrays to standard python lists/tuples
        times = group["time"].values
        xs = group["x"].values * scale
        ys = group["y"].values * scale
        zs = group["z"].values * scale
        
        # B. Create position keyframes as list of tuples: [(t, x, y, z), (t, x, y, z)...]
        p.keyframes = list(zip(times, xs, ys, zs))
        
        # C. Alpha keyframes
        stages = group["lifecycle_stage"].values
        
        alphas = [
            STAGE_TO_ALPHA.get(int(stage), 1.0)
            for stage in stages
        ]
        
        # D. Create alpha keyframes as list of tuples: [(t, alpha), (t, alpha)...]
        p.alpha_keyframes = list(zip(times, alphas))
        
        # E. Add particle object to list and return it
        particles.append(p)

    return particles


### Check if all particles exist for entire simulation ###
def check_particle_lifetimes(df):
    grouped = df.groupby("particle_id")["time"]
    
    summary = grouped.agg(["min", "max", "count"]).reset_index()
    
    all_frames = set(df["time"].unique())
    total_frames = len(all_frames)
    
    summary["exists_full_sim"] = summary["count"] == total_frames
    
    missing_info = []

    for pid, group in df.groupby("particle_id"):
        particle_frames = set(group["time"])
        missing_frames = sorted(all_frames - particle_frames)
        
        if missing_frames:
            missing_info.append({
                "particle_id": pid,
                "missing_frames": missing_frames
            })
    
    missing_df = pd.DataFrame(missing_info)
    
    missing_df["first_frame"] = missing_df["particle_id"].map(
    summary.set_index("particle_id")["min"]
    )

    print(missing_df[["particle_id", "first_frame", "missing_frames"]])
    
    print(f"Total particles: {len(summary)}")
    print(f"Particles missing frames: {len(missing_df)}")
    
    return summary, missing_df


## --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     # 1. Load
#     raw_df = load_all_data("/home/lutra/Documents/BA/lutra_project/blender/example/data/particles")

#     # 2. Physics & Logic Fixes (Pandas)
#     print("Fixing paths...")
#     df = make_path_continous(raw_df, RAW_BOX_SIZE)
#     df = adjust_copio_paths(df)

#     # 3. Create Objects (Python Classes)
#     particles = create_particle_objects(df)

#     print(f"Done. Created {len(particles)} particles.")
#     print(f"Sample: {particles[0].get_name()} is a {type(particles[0]).__name__}")
#     if particles[0].keyframes:
#         print(f"Has {len(particles[0].keyframes)} keyframes.")
