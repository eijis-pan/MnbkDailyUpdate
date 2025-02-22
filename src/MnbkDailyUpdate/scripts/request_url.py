import os
import time
import requests
import json
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT

logger = getLogger(__name__)
logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
# handler.setLevel(INFO)
handler.setLevel(DEBUG)
logger.addHandler(handler)


# Apps Script の doGet() で json データを取得する
def get_json(name=None) -> any:
    token = os.environ.get("GSP_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "v2RecentSearchPython"}
    params = {}

    if name:
        params["player_name"] = name

    # all players (no param)
    url = os.environ.get("MNBK_SPREADSHEET_DEPLOY_URL")

    start = time.time()
    response = requests.get(url, headers=headers, params=params, timeout=(10, 30)) # conn, read
    end = time.time()
    logger.debug(end - start)

    logger.debug(response.status_code)

    response.raise_for_status()

    if response.status_code == 200:
        json_content = json.loads(response.text)
        return json_content

    return None
