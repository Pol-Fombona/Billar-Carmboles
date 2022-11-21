import pandas as pd
from pathlib import Path
from datetime import datetime
import zipfile as zp
import os


def save_game_record_to_pickle(df):
    # Saves game data as pickle format with zip compression

    try:
        filename = "GameData/Replays/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")# + ".pkl"
        filepath_pkl = Path(filename + ".pkl")
        filepath_zip = Path(filename + ".zip")

        filepath_pkl.parent.mkdir(parents=True, exist_ok=True)
        df.to_pickle(filepath_pkl)

        with zp.ZipFile(filepath_zip, "w", zp.ZIP_DEFLATED) as zip_file:
            zip_file.write(filepath_pkl, filename.split("/")[2]+".pkl")

        os.remove(filepath_pkl) # Removes pkl file since zip was created

    except:
        print("Error while saving game replay")

    return

def clean_replay_data_file(file):
    # Removes "pkl" file unzipped

    try:
        file = file.split("zip")[0] + "pkl"
        os.remove(file)

    except:
        print("File", file, "does not exist")
    
    return
    

def load_replay_data(file):
    # Unzips replay data and returns pd Dataframe
    # load from pickle
    
    try:
        path_to_unzip = file.rsplit("\\",1)[0]
        path_to_df = file.split("zip")[0] + "pkl"

        with zp.ZipFile(file, "r") as zip_file:
            zip_file.extractall(path_to_unzip)

        df = pd.read_pickle(path_to_df)
        
        return df

    except:
        print("File", file, "does not exist")
        return None
    

def get_game_replay_data(file):
    # Returns panda dataframe with game data
    # If file does not exist returns None 

    try:

        df = pd.read_pickle(file)
        return df

    except:

        print("File name does not exist")
        return None





