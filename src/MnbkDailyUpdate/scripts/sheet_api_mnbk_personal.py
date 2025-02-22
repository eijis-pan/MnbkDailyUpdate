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

RequestIntervalSeconds = 1
PersonaDataSheetName = "個人データ"
EntryPlayerCol = "A"
EntryPlayerStartRow = 2
EntryPlayerRowSkip = 5
EntryPlayerCheckMaxRow = 1000
BattledPlayerStartColIndex = 4 # "D"
BattledPlayerCheckMaxColIndex  = 1000

# 対戦済みプレイヤー名のリストを取得する
def get_battled_player_list(spread_sheet: Spreadsheet, index: int) -> list:
    work_sheet = spread_sheet.worksheet(PersonaDataSheetName)

    start = time.time()
    player_list = []
    row = EntryPlayerStartRow + (index * EntryPlayerRowSkip)
    i = 0
    for col in range(BattledPlayerStartColIndex, BattledPlayerCheckMaxColIndex):
        if i > 0:
            time.sleep(RequestIntervalSeconds)

        try:
            player_name = work_sheet.cell(row, col).value
        except gspread.exceptions.APIError as e:
            logger.error(f"{e.code} {e.response.reason}")
            break

        if not player_name:
            break
        logger.debug(player_name)
        player_list.append(player_name)
        i += 1

    end = time.time()
    logger.debug(end - start)
    return player_list

# エントリー済みプレイヤー名のリストを取得する
def get_entry_player_list(spread_sheet: Spreadsheet) -> dict:
    work_sheet = spread_sheet.worksheet(PersonaDataSheetName)

    start = time.time()
    player_list = {}
    i = 0
    for row in range(EntryPlayerStartRow, EntryPlayerCheckMaxRow, EntryPlayerRowSkip):
        cell = f"{EntryPlayerCol}{row}"

        if i > 0:
            time.sleep(RequestIntervalSeconds)

        try:
            player_name = work_sheet.acell(cell).value
        except gspread.exceptions.APIError as e:
            logger.error(e.response.reason)
            break

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
