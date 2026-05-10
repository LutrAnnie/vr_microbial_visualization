#This script takes the grid data from our csv files and
#converts it to the openvdb format

import csv
import os
import numpy as np # type: ignore
import pyopenvdb as openvdb # type: ignore
import math

def apply_csv_to_openvdb():
    
    print("Starting csv to openvdb...")

    #renamed FIELDNAMES to CSV_HEADERS
    CSV_HEADERS = [
        "_timestep",
        "box_id_x",
        "box_id_y",
        "box_id_z",
        "_x_center",
        "_y_center",
        "_z_center",
        "concentration"
    ]


    ### TESTING ###
    DATA_LOCATION = "/home/lutra/Documents/BA/data_1000"
    ### END ####
    
    #DATA_LOCATION = os.environ['DATA_LOCATION']
    print(f"The data location is {DATA_LOCATION}")

    def load_volume(file_path, highest_concentration, lowest_concentration):
        Volume = np.zeros([56, 56, 56])
        with open(file_path, "r") as file:
            reader = csv.DictReader(
                file,     
                fieldnames = CSV_HEADERS, #fieldnames is a variable i cannot control
                delimiter = ",",
            )
            for row in reader:
                row = cast_fields(row)
                Volume[row["box_id_x"] - 1, row["box_id_y"] - 1, row["box_id_z"] - 1] = ( # type: ignore
                    transform_concentration(
                        row["concentration"], highest_concentration, lowest_concentration
                    ) 
                )
        return Volume

    def cast_fields(fields):
        fields["box_id_x"] = int(fields["box_id_x"])
        fields["box_id_y"] = int(fields["box_id_y"])
        fields["box_id_z"] = int(fields["box_id_z"])
        fields["concentration"] = float(fields["concentration"])
        return fields


    # all values are between 0 and 1 with log10 scaling
    def transform_concentration(concentration, highest_concentration, lowest_concentration):
        #check for invalid data inputs
        try:
            if concentration <= 0:
                raise ValueError(f"Invalid concentration: {concentration}")
            if lowest_concentration <= 0 or highest_concentration <= 0:
                raise ValueError(f"Invalid lowest_concentration: {lowest_concentration} or highest_concentration: {highest_concentration}")
            if highest_concentration == lowest_concentration:
                raise ValueError(f"highest_concentration: {highest_concentration} is equal to lowest_concentration: {lowest_concentration}")
        
            #Proceed with computation
            return (math.log10(concentration / lowest_concentration)) / (
                math.log10(highest_concentration / lowest_concentration)
            )
        
        except Exception as e:
            print(f"[ERROR] Problem with values: conc = {concentration}, high = {highest_concentration}, low = {lowest_concentration}")
            raise e


    def create_grid(Volume, i):
        grid = openvdb.FloatGrid()
        grid.copyFromArray(Volume.astype(float))
        grid.transform = openvdb.createLinearTransform(
            [[0.25, 0, 0, 0], [0, 0.25, 0, 0], [0, 0, 0.25, 0], [0, 0, 0, 1]]
        )
        grid.gridClass = openvdb.GridClass.FOG_VOLUME
        grid.name = "density"
        #BEST PRACTICE - string concatenation and path.join() for cross platfrom handling:
        path_to_grid = os.path.join(DATA_LOCATION, f"grid/grid-{i}.vdb")
        openvdb.write(path_to_grid, grid)

    i =1 
    highest_concentration = 0
    lowest_concentration = 100000

    while True:
        file_path = os.path.join(DATA_LOCATION, f"grid/grid-{i}.csv")
    
        #stop looping once path does not exist anymore
        if not os.path.exists(file_path):
            print(f"[INFO] No more files as grid-{i-1}. Stopping.")
            break
        
        with open(file_path, "r") as file:
            reader = csv.DictReader(
                file, 
                fieldnames = CSV_HEADERS,
                delimiter = ","
            )
            for row in reader:
                row = cast_fields(row)
                if row["concentration"] > highest_concentration: # type: ignore
                    highest_concentration = row["concentration"]
                if row["concentration"] < lowest_concentration: # type: ignore
                    lowest_concentration = row["concentration"]
        
        print(
            f"highest: {highest_concentration}, lowest: {lowest_concentration}"
        )
        
        i += 1
        
    j = 1

    while True:
        file_path = os.path.join(DATA_LOCATION, f"grid/grid-{j}.csv")
        
        #stop looping once path does not exist anymore
        if not os.path.exists(file_path):
            print(f"[INFO] Finished creating grids. Stopped at grid-{j-1}.")
            break
        
        print(f"Loading: {file_path}")
        #print('loading ' + file_path)
        Volume = load_volume(file_path, highest_concentration, lowest_concentration)
        create_grid(Volume, str(j))
        
        j += 1

if __name__ == "__main__":      
    apply_csv_to_openvdb()

