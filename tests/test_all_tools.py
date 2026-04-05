#!/usr/bin/env python3
"""
端對端測試 — 驗證所有 Tools 可正常呼叫 91app Admin API 並回傳結果
"""
import sys
import os
import json
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 匯入工具模組以觸發 @mcp.tool() 裝飾器的副作用（工具註冊）
import tools.order_tools       # noqa: F401
import tools.product_tools     # noqa: F401
import tools.promotion_tools   # noqa: F401
import tools.delivery_tools    # noqa: F401

from tools.order_tools import (
    get_order_list,
    get_order_detail,
    get_return_order_list,
    get_return_order_detail,
    get_exchange_order_list,
)
from tools.product_tools import (
    get_product_list,
    get_product_detail,
    get_product_stock,
    get_shop_categories,
    get_category_tree,
    get_shop_payment_methods,
    get_shop_shipping_methods,
)
from tools.promotion_tools import (
    get_promotions,
    get_promotion_detail,
    get_promotion_salepages,
)
from tools.delivery_tools import (
    get_shipping_order,
    get_shipping_countries,
)
from app import mcp
import config.settings as settings
import asyncio


def run_test(name, fn, **kwargs):
    """執行一個 Tool 並印出結果摘要"""
    print(f"\n{'─' * 50}")
    print(f"🔧 {name}")
    print(f"   params: {kwargs}")
    try:
        result = fn(**kwargs)
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False

        # 印出 key-level 摘要
        for k, v in result.items():
            if isinstance(v, list):
                print(f"   {k}: [{len(v)} items]")
                if v and len(v) > 0:
                    first = v[0]
                    if isinstance(first, dict):
                        print(f"     first: {json.dumps(first, ensure_ascii=False)[:200]}")
            elif isinstance(v, dict) and len(str(v)) > 200:
                print(f"   {k}: {{...{len(v)} keys}}")
            else:
                print(f"   {k}: {v}")

        print(f"   ✅ OK")
        return True
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("91app Admin API Tools 端對端測試")
    print("=" * 60)
    print(f"BASE_URL : {settings.BASE_URL}")
    print(f"SHOP_ID  : {settings.SHOP_ID}")
    print(f"API_KEY  : {'***' + settings.API_KEY[-4:] if len(settings.API_KEY) > 4 else '(not set)'}")

    # 確認工具數量
    tools_list = asyncio.run(mcp.list_tools())
    print(f"\n共 {len(tools_list)} 個 Tools 待測試\n")

    results = {}

    # --- 商店設定類（不需日期參數）---
    results["get_shop_payment_methods"] = run_test(
        "get_shop_payment_methods", get_shop_payment_methods,
    )
    results["get_shop_shipping_methods"] = run_test(
        "get_shop_shipping_methods", get_shop_shipping_methods,
    )
    results["get_shop_categories"] = run_test(
        "get_shop_categories", get_shop_categories,
    )
    results["get_category_tree"] = run_test(
        "get_category_tree", get_category_tree,
    )
    results["get_shipping_countries"] = run_test(
        "get_shipping_countries", get_shipping_countries,
    )

    # --- 商品類 ---
    results["get_product_list"] = run_test(
        "get_product_list", get_product_list,
        start_date="2024-01-01", end_date="2024-01-07", count=5,
    )

    # --- 訂單類 ---
    results["get_order_list"] = run_test(
        "get_order_list", get_order_list,
        start_date="2024-01-01", end_date="2024-01-07", count=5,
    )

    # --- 促銷類 ---
    results["get_promotions"] = run_test(
        "get_promotions", get_promotions,
    )

    # 摘要
    print("\n" + "=" * 60)
    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    print(f"結果: {passed} 通過, {failed} 失敗 / 共 {len(results)} 項")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
