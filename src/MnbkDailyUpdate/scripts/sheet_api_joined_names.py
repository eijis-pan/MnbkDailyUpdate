import time

import gspread
from gspread import Spreadsheet
import json
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT


logger = getLogger(__name__)
logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(DEBUG)
logger.addHandler(handler)

RequestIntervalSeconds = 2
PersonaDataSheetName = "シート18"
EntryPlayerCell = "A1"
BattledPlayerStartCol = "C"
BattledPlayerStartRow = 2
BattledPlayerRowSkip = 5
BattledPlayerCheckMaxRow  = 1000


# タブで連結された対戦済みプレイヤー名のリストを取得する
def get_battled_player_list(spread_sheet: Spreadsheet, index: int) -> list:
    work_sheet = spread_sheet.worksheet(PersonaDataSheetName)

    start = time.time()
    player_list = []

    row = BattledPlayerStartRow + (index * BattledPlayerRowSkip)
    cell = f"{BattledPlayerStartCol}{row}"

    if index > 0:
        time.sleep(RequestIntervalSeconds)

    player_names = None
    try:
        player_names = work_sheet.acell(cell).value
    except gspread.exceptions.APIError as e:
        logger.error(e.response.reason)

    if player_names is None:
        return player_list

    i = 0
    for player_name in player_names.split("\t"):
        if i == 0 and 0 < len(player_name):
            continue
        if not player_name:
            break
        logger.debug(player_name)
        player_list.append(player_name)
        i += 1

    end = time.time()
    logger.debug(end - start)
    return player_list

# タブで連結されたエントリー済みプレイヤー名のリストを取得する
def get_entry_player_list(spread_sheet: Spreadsheet) -> dict:
    work_sheet = spread_sheet.worksheet(PersonaDataSheetName)

    start = time.time()
    player_list = {}

    player_names = None
    try:
        player_names = work_sheet.acell(EntryPlayerCell).value
    except gspread.exceptions.APIError as e:
        logger.error(e.response.reason)

    if player_names is None:
        return player_list

    i = 0
    for player_name in player_names.split("\t"):
        if not player_name:
            break
        logger.debug(player_name)
        player_list[player_name] = i
        i += 1

    end = time.time()
    logger.debug(end - start)
    return player_list

def get_json(spread_sheet: Spreadsheet, name=None) -> str:
    if name is None:
        player_list = get_entry_player_list(spread_sheet)
    else:
        player_list = get_battled_player_list(spread_sheet, name)
    return json.dumps(player_list, ensure_ascii=False)
