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

if __name__ == "__main__":
    try:
        entryPlayerList = get_json()
        logger.debug(entryPlayerList)
    except Exception as e:
        logger.error("データ取得に失敗")
        exit(1)

    nameWithIndex = {}
    i = 0
    for entryPlayer in entryPlayerList:
        # nameWithHash[entryPlayer] = f"{hash(entryPlayer):X}"
        nameWithIndex[entryPlayer] = i
        i += 1

    try:
        with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="w", encoding="utf-8") as file:
            json.dump(nameWithIndex, file, ensure_ascii=False)
    except Exception as e:
        logger.error("データファイル作成に失敗")
        exit(2)
