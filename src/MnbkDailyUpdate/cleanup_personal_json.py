from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT

import config
from scripts.cleanup_personal_file import cleanup_battled_json

logger = getLogger(__name__)
logger.setLevel(INFO)
# logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)

if __name__ == "__main__":
    cleanup_battled_json(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT)

