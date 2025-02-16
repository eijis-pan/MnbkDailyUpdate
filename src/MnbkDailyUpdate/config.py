import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ENTRY_PLAYER_LIST_FILE_PATH = os.path.join(DATA_DIR, "entry_player_list.json")
PLAYER_BATTLED_LIST_FILE_PATH_FMT = os.path.join(DATA_DIR, "player_battled_list_{0}.json")
