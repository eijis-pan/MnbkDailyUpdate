import base64
import os
import json
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter, BASIC_FORMAT

logger = getLogger(__name__)
logger.setLevel(DEBUG)

handler = StreamHandler()
handler.setFormatter(Formatter(BASIC_FORMAT))
handler.setLevel(INFO)
# handler.setLevel(DEBUG)
logger.addHandler(handler)


# PRIVATE KEY の json データを環境変数から作成
def get_google_auth_settngs() -> dict[str, str]:
    google_auth_settngs = {
        "type": "service_account",
        "project_id": os.environ.get("GCP_PROJECT_ID"),
        "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
        "private_key":  base64.standard_b64decode(os.environ.get("GCP_PRIVATE_KEY")).decode('ascii'),
        "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
        "client_id": os.environ.get("GCP_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("GCP_CLIENT_X509_CERT_URL"),
        "universe_domain": "googleapis.com"
    }
    return google_auth_settngs
