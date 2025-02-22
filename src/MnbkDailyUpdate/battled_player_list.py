from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT
import json

import config
from scripts.request_url import get_json

logger = getLogger(__name__)
logger.setLevel(INFO)
# logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)

def battled_player_list(name: str, index: int):
    try:
        battledPlayerList = get_json(name)
        logger.debug(battledPlayerList)
    except Exception as e:
        logger.error(f"対戦済みデータ取得に失敗 [ {name} ]")
        return 1

    try:
        with open(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT.format(index), mode="w", encoding="utf-8") as file:
            json.dump(battledPlayerList, file, ensure_ascii=False)
    except Exception as e:
        logger.error(f"対戦済みデータファイル作成に失敗 [ {name} ]")
        return 2

    return 0

if __name__ == "__main__":

    try:
        with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="r", encoding="utf-8") as file:
            entryPlayerList = json.load(file)
    except Exception as e:
        logger.error("エントリー済みプレイヤーリストファイル読み込みに失敗")
        exit(3)

    ret = 0
    for entryPlayer in entryPlayerList:
        index = entryPlayerList[entryPlayer]
        ret = battled_player_list(entryPlayer, index)

    exit(ret)

