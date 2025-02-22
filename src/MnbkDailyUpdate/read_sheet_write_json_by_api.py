import json
import tempfile
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT
import gspread
from google.auth import exceptions
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import storage
import os

import config
from scripts.google_auth import get_google_auth_settngs
# from scripts.sheet_api_mnbk_personal import (get_entry_player_list, get_battled_player_list)
from scripts.sheet_api_joined_names import (get_entry_player_list, get_battled_player_list)

logger = getLogger(__name__)
logger.setLevel(INFO)
# logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)

if __name__ == "__main__":

    auth_settings = get_google_auth_settngs()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
        json.dump(auth_settings, file)
        authJsonPath = file.name
        file.close()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = authJsonPath

    try:
        # credentials = ServiceAccountCredentials.from_json_keyfile_dict(auth_settings, scope)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(authJsonPath, scope)
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        client = gspread.authorize(credentials)
    except exceptions.DefaultCredentialsError as e:
        logger.error(f"Google認証に失敗")
        exit(1)
    finally:
        os.remove(authJsonPath)

    try:
        spread_sheet = client.open_by_key(os.environ['MNBK_SPREADSHEET_ID'])
    except Exception as e:
        logger.error("Google SpreadSheet が見つからないかアクセス権限がありません")
        exit(2)

    try:
        nameWithIndex = get_entry_player_list(spread_sheet)
    except Exception as e:
        logger.error("エントリー済みプレイヤーリスト取得に失敗")
        exit(3)

    try:
        with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="w", encoding="utf-8") as file:
            json.dump(nameWithIndex, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
    except Exception as e:
        logger.error("エントリー済みプレイヤーリストデータファイル作成に失敗")
        exit(4)

    # try:
    #     with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="r", encoding="utf-8") as file:
    #         nameWithIndex = json.load(file)
    # except Exception as e:
    #     logger.error("エントリー済みプレイヤーリストファイル読み込みに失敗")
    #     exit(3)

    for name in nameWithIndex:
        index = nameWithIndex[name]
        logger.debug(f"対戦済みデータ取得 {name} [{index}]")
        try:
            names = get_battled_player_list(spread_sheet, index)
        except Exception as e:
            logger.error(f"対戦済みデータ取得に失敗 [ {name} ]")
            exit(5)

        if len(names) == 0:
            continue

        try:
            with open(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT.format(index), mode="w", encoding="utf-8") as file:
                json.dump(names, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
        except Exception as e:
            logger.error(f"対戦済みデータファイル作成に失敗 [ {name} ]")
            exit(6)
