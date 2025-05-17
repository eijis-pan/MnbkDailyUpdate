import time
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
from scripts.sheet_api_joined_names import (get_entry_player_list, get_battled_player_list, EntrySheetName, PersonaDataSheetName)
from scripts.cleanup_personal_file import cleanup_battled_json

logger = getLogger(__name__)
# logger.setLevel(INFO)
logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
# handler.setLevel(INFO)
handler.setLevel(DEBUG)
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
        nameWithIndex = get_entry_player_list(spread_sheet, EntrySheetName)
    except Exception as e:
        logger.error("エントリー済みプレイヤーリスト取得に失敗")
        exit(3)

    # 対戦済みリストのインデックス部分を取得する
    try:
        nameWithIndex_battled = get_entry_player_list(spread_sheet, PersonaDataSheetName)
    except Exception as e:
        logger.error("対戦済みリストのインデックス取得に失敗")
        exit(8)

    # エントリー済みプレイヤー名のリストを対戦済みリストのインデックスに付け替える
    max_battled_index = -1
    for name in nameWithIndex:
        if name in nameWithIndex_battled:
            battled_index = nameWithIndex_battled[name]
            nameWithIndex[name] = battled_index
            if max_battled_index < battled_index:
                max_battled_index = battled_index
        else:
            nameWithIndex[name] = -1

    empty_names = []
    for (name, battled_index) in nameWithIndex.items():
        if battled_index < 0:
            max_battled_index += 1
            nameWithIndex[name] = max_battled_index
            empty_names.append(name)

    namesWithTimestamp = {
        "timestamp": int(time.time()),
        "entry_player_list": nameWithIndex,
    }

    try:
        with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="w", encoding="utf-8") as file:
            # json.dump(nameWithIndex, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
            json.dump(namesWithTimestamp, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
    except Exception as e:
        logger.error("エントリー済みプレイヤーリストデータファイル作成に失敗")
        exit(4)

    # try:
    #     with open(config.ENTRY_PLAYER_LIST_FILE_PATH, mode="r", encoding="utf-8") as file:
    #         nameWithIndex = json.load(file)
    # except Exception as e:
    #     logger.error("エントリー済みプレイヤーリストファイル読み込みに失敗")
    #     exit(3)

    cleanup_battled_json(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT)

    for name in nameWithIndex:
        if name in empty_names:
            continue

        index = nameWithIndex[name]
        if index < 0:
            continue

        logger.debug(f"対戦済みデータ取得 {name} [{index}]")
        try:
            names = get_battled_player_list(spread_sheet, index)
        except Exception as e:
            logger.error(f"対戦済みデータ取得に失敗 [ {name} ]")
            exit(5)

        logger.debug(names)
        if len(names) == 0:
            continue

        try:
            with open(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT.format(index), mode="w", encoding="utf-8") as file:
                json.dump(names, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
            # file = open(config.PLAYER_BATTLED_LIST_FILE_PATH_FMT.format(index), mode="w", encoding="utf-8")
            # json.dump(names, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
        except Exception as e:
            logger.error(f"対戦済みデータファイル作成に失敗 [ {name} ]")
            exit(6)
        # finally:
        #     if file:
        #         file.close()

    # try:
    #     with open(config.TIMESTAMP_FILE_PATH, mode="w", encoding="utf-8") as file:
    #         json.dump({"timestamp":int(time.time())}, file, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
    # except Exception as e:
    #     logger.error("データ更新タイムスタンプファイル作成に失敗")
    #     exit(7)
