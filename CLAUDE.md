# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

91app Admin API MCP Server。將 91app Admin API 封裝為 17 個 AI Agent 可呼叫的查詢工具（訂單、商品、促銷、配送）。透過 stdio MCP server 供 Claude Code / Cowork 整合使用。

程式碼註解與工具描述使用繁體中文（zh-Hant）。外部依賴：`requests`、`pydantic`。

## Setup & Running

```bash
pip install -e .
cp .env.example .env
# 將 API key 和 Shop ID 填入 .env
export APP_91APP_API_KEY=your_api_key_here
export APP_91APP_BASE_URL=https://api.91app.com
export APP_91APP_SHOP_ID=your_shop_id

# 啟動 MCP server（stdio JSON-RPC 2.0）
python mcp_server.py

# 或透過 .mcp.json 自動偵測
```

## Running Tests

```bash
# 端對端測試（17 個工具，呼叫 live API）
python tests/test_all_tools.py

# API 連線驗證
python scripts/auth/test_connection.py

# 探測 API 回應結構
python scripts/auth/inspect_data_structure.py
```

無測試框架 — 測試為獨立 script。所有測試皆呼叫 live API，需設定環境變數。

## Architecture

所有 91app Admin API 端點均使用 **POST + JSON body**（包含查詢操作），無 HTTP GET 端點。

### Request Flow

`mcp_server.py` (stdin JSON-RPC) → `tools/*_tools.py` (@mcp.tool() 函式) → `base_tool.py` (api_post HTTP client) → `config/settings.py` (URL + auth)

### API Layer (`config/` + `tools/base_tool.py`)

- `config/settings.py` — API base URL、API key from env、endpoint map（`ENDPOINTS` dict）、`get_headers()`、`get_url()`
- `tools/base_tool.py` — 共用 HTTP client，`api_post()` 含自動重試（指數退避）、91app 回應封包正規化

### Response Envelope

```json
{
  "Status": "Success" | "Error",
  "Data": { ... } | [ ... ],
  "ErrorMessage": "",
  "TimeStamp": "2024-..."
}
```

`api_post()` 自動將 `Status: "Error"` 轉為 `{"error": ..., "code": 400}` 標準錯誤格式。

### Tools Layer (`tools/`)

每個 tool module 使用 `@mcp.tool()` 裝飾器註冊工具：

- `order_tools.py` (5): get_order_list, get_order_detail, get_return_order_list, get_return_order_detail, get_exchange_order_list
- `product_tools.py` (7): get_product_list, get_product_detail, get_product_stock, get_shop_categories, get_category_tree, get_shop_payment_methods, get_shop_shipping_methods
- `promotion_tools.py` (3): get_promotions, get_promotion_detail, get_promotion_salepages
- `delivery_tools.py` (2): get_shipping_order, get_shipping_countries

## Project Structure

```
mcp-91app/
├── mcp_server.py          — stdio 入口；import tool 模組觸發 @mcp.tool() 副作用
├── app.py                 — MCPServer 單例
├── config/settings.py     — env vars, ENDPOINTS, get_headers()
├── tools/
│   ├── base_tool.py       — api_post() 共用 HTTP client
│   ├── order_tools.py     — 5 個訂單查詢工具
│   ├── product_tools.py   — 7 個商品/庫存查詢工具
│   ├── promotion_tools.py — 3 個促銷查詢工具
│   └── delivery_tools.py  — 2 個配送查詢工具
├── _spec/
│   ├── api-tools-list.md     — API 端點完整盤點
│   └── tool-manifest.json    — 機器可讀工具規格
├── tests/test_all_tools.py   — 獨立測試 script
└── scripts/auth/
    ├── test_connection.py    — 連線驗證
    └── inspect_data_structure.py — 回應結構探測
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `APP_91APP_API_KEY` | ✅ | 從 91APP OMNI 管理後台取得 |
| `APP_91APP_BASE_URL` | ✅ | API base URL（正式或沙盒環境） |
| `APP_91APP_SHOP_ID` | 建議設定 | 各 API 呼叫的預設 ShopId |

## Adding New Tools

1. 從 https://developer.91app.com/zh-tw/ 確認端點
2. 在 `config/settings.py::ENDPOINTS` 新增端點
3. 在對應的 `tools/{domain}_tools.py` 加入 `@mcp.tool()` 函式
4. 在 `tests/test_all_tools.py` 加入測試
5. 更新 `_spec/api-tools-list.md`
