#!/usr/bin/env python3
"""
91app Admin API MCP Server — 供 Claude Code / Claude Cowork 調用

透過 MCP Python SDK stdio 傳輸，暴露 91app Admin API 查詢工具。
涵蓋 16 個 API 分類、4 種認證方式。

使用方式:
  1. 在 .mcp.json 中設定（見專案根目錄範例）
  2. 或手動啟動: python mcp_server.py
"""
import sys
import os

# 確保能 import tools 模組與 app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 匯入工具模組以觸發 @mcp.tool() 裝飾器的副作用（工具註冊）
# --- Cat.1-9: x-api-key ---
import tools.order_tools           # noqa: F401  Cat.1 Order (13 tools)
import tools.delivery_tools        # noqa: F401  Cat.2 Delivery (12 tools)
import tools.product_tools         # noqa: F401  Cat.3 SalePage (14 tools)
import tools.promotion_tools       # noqa: F401  Cat.4 Promotion (9 tools)
import tools.location_tools        # noqa: F401  Cat.5 Location (2 tools)
import tools.multilingual_tools    # noqa: F401  Cat.7 Multilingual (1 tool)
import tools.pos_tools             # noqa: F401  Cat.8 POS (6 tools)
import tools.invoice_tools         # noqa: F401  Cat.9 Invoice (7 tools)
# --- Cat.10-11: n1-api-key ---
import tools.ims_brand_tools       # noqa: F401  Cat.10 IMS Brand (11 tools)
import tools.ims_channel_tools     # noqa: F401  Cat.11 IMS Channel (9 tools)
# --- Cat.12-13: HMAC ---
import tools.payment_tools         # noqa: F401  Cat.12+13 Payments (11 tools)
# --- Cat.14: ny-api-token ---
import tools.member_tools          # noqa: F401  Cat.14 Member CC (8 tools)

from app import mcp


def main():
    mcp.run()  # 預設 stdio transport


if __name__ == "__main__":
    main()
