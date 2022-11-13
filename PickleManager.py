import pandas as pd
from pathlib import Path
from datetime import datetime


def save_game_record_to_pickle(df):
    # Saves game data as pickle format with bz2 compression

    # 5 min aprox de partida: 19362 rows
    #   csv: 1.3 Mb
    #   pickle: 2.63 Mb

    filename = "GameData/Replays/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pkl"
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_pickle(filepath)

    return


def get_game_replay_data(file):
    # Returns panda dataframe with game data
    # If file does not exist returns None 

    try:

        df = pd.read_pickle(file)
        return df

    except:

        print("File name does not exist")
        return None





