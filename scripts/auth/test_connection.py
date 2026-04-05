#!/usr/bin/env python3
"""
Step 1: API 連線驗證
- 測試 API Key 有效性
- 確認基本端點可存取
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
import config.settings as settings


def test_connection():
    """測試 API 連線與 API Key 有效性"""
    print("=" * 60)
    print("Step 1: 91app Admin API 連線驗證")
    print("=" * 60)
    print(f"\nBASE_URL : {settings.BASE_URL}")
    print(f"SHOP_ID  : {settings.SHOP_ID}")
    print(f"API_KEY  : {'***' + settings.API_KEY[-4:] if len(settings.API_KEY) > 4 else '(not set)'}")

    if not settings.API_KEY:
        print("\n❌ APP_91APP_API_KEY 環境變數未設定。")
        sys.exit(1)

    # 使用輕量端點測試連線
    url = f"{settings.BASE_URL.rstrip('/')}/ec/V1/Shop/GetPayment"
    headers = settings.get_headers()

    print(f"\n[1] 測試端點: POST {url}")
    try:
        resp = requests.post(url, json={}, headers=headers, timeout=30)
        print(f"    Status: {resp.status_code}")
        data = resp.json()
        status = data.get("Status", "unknown")
        print(f"    API Status: {status}")
        if status == "Success":
            print(f"\n    ✅ 連線成功!")
        else:
            print(f"\n    ❌ API 回傳錯誤: {data.get('ErrorMessage', 'unknown')}")
    except Exception as exc:
        print(f"\n    ❌ 連線失敗: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    test_connection()
