#!/usr/bin/env python3
"""
Inspect 91app API response structures for a given endpoint.
Useful during development to understand data shapes.

Usage:
    python scripts/auth/inspect_data_structure.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.base_tool import api_post
import config.settings as settings


def inspect(endpoint_key: str, payload: dict):
    print(f"\nEndpoint: {endpoint_key}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    print("-" * 50)
    result = api_post(endpoint_key, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    shop_id = settings.SHOP_ID or 0

    # --- Inspect shop config endpoints ---
    inspect("shop_payment_methods", {})
    inspect("shop_categories", {"ShopId": shop_id})
    inspect("shipping_countries", {"ShopId": shop_id})
