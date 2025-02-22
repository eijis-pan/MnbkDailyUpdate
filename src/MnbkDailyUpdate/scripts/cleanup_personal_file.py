import json
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT

logger = getLogger(__name__)
logger.setLevel(INFO)
# logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)

BattledPlayerMaxCount = 100 # 0..99

# 対戦済みプレイヤー名のファイルを空にする
def cleanup_battled_json(file_name_fmt) -> None:
    for index in range(0, BattledPlayerMaxCount):
        with open(file_name_fmt.format(index), mode="w", encoding="utf-8") as file:
            json.dump([], file)
