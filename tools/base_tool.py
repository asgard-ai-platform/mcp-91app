"""
91app Admin API 基底工具 — HTTP 請求、重試、錯誤處理共用邏輯

Cat.1-9：所有端點均使用 POST + JSON body（包含查詢操作）。
Cat.10-14：使用標準 REST（GET/POST/PUT/DELETE/PATCH）。
"""
import sys
import os
import json
import time
from urllib.parse import quote

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests

from config.settings import (
    get_headers, get_headers_n1, get_headers_hmac, get_headers_member,
    get_url, get_ims_url, get_payments_url, get_member_url,
)


def _normalize_response(data):
    """正規化 91app 回應封包：將 Status=Error 轉為標準錯誤格式"""
    if isinstance(data, dict) and data.get("Status") == "Error":
        return {
            "error": data.get("ErrorMessage", "API returned Error status"),
            "code": 400,
            "raw": data,
        }
    return data


def _retry_request(request_fn, retries=3):
    """帶重試的 HTTP 請求執行器"""
    for attempt in range(retries):
        try:
            response = request_fn()
            response.raise_for_status()
            data = response.json()
            return _normalize_response(data)
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response else 0
            if status < 500 or attempt == retries - 1:
                return {"error": str(exc), "code": status}
            time.sleep(2**attempt)
        except requests.exceptions.RequestException as exc:
            if attempt == retries - 1:
                return {"error": str(exc), "code": 0}
            time.sleep(2**attempt)

    return {"error": "Max retries exceeded", "code": 0}


# ============================================================
# Cat.1-9: POST + x-api-key
# ============================================================

def api_post(endpoint_key, payload, retries=3):
    """發送 POST 請求到 91app Admin API（Cat.1-9），回傳 JSON。含自動重試。"""
    url = get_url(endpoint_key)
    headers = get_headers()
    return _retry_request(
        lambda: requests.post(url, json=payload, headers=headers, timeout=60),
        retries=retries,
    )


# ============================================================
# Cat.10-11: GET + n1-api-key（IMS Brand / Channel）
# ============================================================

def api_get_ims(endpoint_key, params=None, retries=3, **path_params):
    """發送 GET 請求到 91app IMS API（Cat.10-11），回傳 JSON。"""
    url = get_ims_url(endpoint_key, **path_params)
    headers = get_headers_n1()
    return _retry_request(
        lambda: requests.get(url, params=params, headers=headers, timeout=60),
        retries=retries,
    )


# ============================================================
# Cat.12-13: GET/POST + HMAC-SHA256（Payments）
# ============================================================

def api_get_payments(endpoint_key, params=None, retries=3, **path_params):
    """發送 GET 請求到 91app Payments API（Cat.12-13），回傳 JSON。"""
    url = get_payments_url(endpoint_key, **path_params)
    headers = get_headers_hmac()
    return _retry_request(
        lambda: requests.get(url, params=params, headers=headers, timeout=60),
        retries=retries,
    )


def api_post_payments(endpoint_key, payload, retries=3, **path_params):
    """發送 POST 請求到 91app Payments API（Cat.12-13），回傳 JSON。"""
    url = get_payments_url(endpoint_key, **path_params)
    body = json.dumps(payload, ensure_ascii=False)
    headers = get_headers_hmac(body)
    return _retry_request(
        lambda: requests.post(url, data=body, headers=headers, timeout=60),
        retries=retries,
    )


# ============================================================
# Cat.14: GET + ny-api-token（Member Connect Cloud）
# ============================================================

def api_get_member(endpoint_key, params=None, retries=3, **path_params):
    """發送 GET 請求到 91app Member API（Cat.14），回傳 JSON。"""
    url = get_member_url(endpoint_key, **path_params)
    headers = get_headers_member()
    return _retry_request(
        lambda: requests.get(url, params=params, headers=headers, timeout=60),
        retries=retries,
    )


# ============================================================
# 共用輔助
# ============================================================

def extract_list(result, key="Data"):
    """從 API 回應中提取清單並回傳標準 {"data": [...], "total": N} 格式"""
    if "error" in result:
        return result
    data = result.get(key, {})
    items = data if isinstance(data, list) else data.get("List", data.get("list", []))
    if not isinstance(items, list):
        items = [items] if items else []
    return {"data": items, "total": len(items)}


def extract_detail(result, key="Data"):
    """從 API 回應中提取單筆資料"""
    if "error" in result:
        return result
    return result.get(key, result)
