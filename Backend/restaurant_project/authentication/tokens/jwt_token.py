from datetime import datetime, timedelta, UTC
import json
import uuid
from decouple import config
import hashlib
import hmac
import base64
import helper


def create_jwt_token():
    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    payload = {
        "id": str(uuid.uuid4()),
        "exp": int((datetime.now(UTC) + timedelta(hours=1)).timestamp()),
    }

    payload_json = json.dumps(payload).encode("utf-8")
    encode_payload = base64.urlsafe_b64encode(payload_json).decode("utf-8")
    encode_payload = helper.replace_pattern(encode_payload)

    header_json = json.dumps(header).encode("utf-8")
    encode_header = base64.urlsafe_b64encode(header_json).decode("utf-8")
    encode_header = helper.replace_pattern(encode_header)

    token_data = f"{encode_header}.{encode_payload}"
    secret_key = config("SECRET_KEY").encode("utf-8")

    hmac_encode = hmac.new(secret_key, token_data.encode("utf-8"), hashlib.sha256)
    signature = base64.urlsafe_b64encode(hmac_encode.digest()).decode("utf-8")
    signature = helper.replace_pattern(signature)

    return f"{token_data}.{signature}"


print(create_jwt_token())
