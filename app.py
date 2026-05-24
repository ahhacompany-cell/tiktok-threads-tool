\
from flask import Flask, render_template, request, jsonify
import hmac
import hashlib
import datetime
import requests
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

GPTS_URL = "https://chatgpt.com/g/g-69ef95c18ff081918a267dcbd722305f-sseuredeu-ni-daeboni-nae-daebonida"
LENS_URL = "https://lens.google.com/"
TIKVIDEO_URL = "https://tikvideo.app/ko"

def make_auth(access_key, secret_key, method, path, query=""):
    now = datetime.datetime.utcnow()
    signed_date = now.strftime("%y%m%dT%H%M%SZ")
    message = signed_date + method + path + query
    signature = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return (
        "CEA algorithm=HmacSHA256, "
        f"access-key={access_key}, "
        f"signed-date={signed_date}, "
        f"signature={signature}"
    )

@app.route("/")
def index():
    return render_template("index.html", gpts_url=GPTS_URL, lens_url=LENS_URL, tikvideo_url=TIKVIDEO_URL)

@app.route("/api/deeplink", methods=["POST"])
def deeplink():
    data = request.get_json(force=True)
    access_key = (data.get("accessKey") or "").strip()
    secret_key = (data.get("secretKey") or "").strip()
    coupang_url = (data.get("coupangUrl") or "").strip()

    if not access_key or not secret_key or not coupang_url:
        return jsonify({"ok": False, "error": "Access Key, Secret Key, 쿠팡 링크를 모두 입력하세요."}), 400

    method = "POST"
    path = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    url = "https://api-gateway.coupang.com" + path

    headers = {
        "Authorization": make_auth(access_key, secret_key, method, path),
        "Content-Type": "application/json",
    }

    payload = {"coupangUrls": [coupang_url]}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        try:
            body = r.json()
        except Exception:
            body = {"raw": r.text}

        if not r.ok:
            return jsonify({"ok": False, "status": r.status_code, "error": body}), r.status_code

        item = None
        if isinstance(body, dict):
            data_list = body.get("data")
            if isinstance(data_list, list) and data_list:
                item = data_list[0]

        short_url = ""
        if isinstance(item, dict):
            short_url = item.get("shortenUrl") or item.get("landingUrl") or ""

        if not short_url:
            return jsonify({"ok": False, "error": "쿠파스 링크를 찾지 못했습니다.", "response": body}), 500

        return jsonify({"ok": True, "coupasUrl": short_url, "response": body})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
