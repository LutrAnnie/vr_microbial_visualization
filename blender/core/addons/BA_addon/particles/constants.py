"""
Script stores all constants used in the particle scripts
"""

# --- 1. Particle class constants ---
COPIO = 1
OLIGO = 2
SPHY = 3
MPHY = 4
HEALTHY = [1, 2]
SENESCENT = 3
DEAD = 4

#TODO: radius to diameter
# --- 2. Define CSV headers ---
ROW_ID = "_row_id"
ID = "id"
SPECIES_ID = "species_id"
LIFECYCLE_STAGE = "lifecycle_stage"
X = "x"
Y = "y"
Z = "z"
THETA = "theta"
PHI = "phi"
RADIUS = "radius"

#TODO: radius to diameter
CSV_HEADERS = [
  ROW_ID,
  ID,
  SPECIES_ID,
  LIFECYCLE_STAGE,
  X,
  Y,
  Z,
  THETA,
  PHI,
  RADIUS
]