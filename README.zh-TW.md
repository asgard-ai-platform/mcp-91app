# mcp-91app

91app Admin API MCP Server — 僅包含查詢（Get）類工具，共 **17 個工具**，涵蓋訂單、商品、促銷、物流查詢。

## 快速開始

```bash
cd mcp-servers/mcp-91app
pip install -e .
cp .env.example .env
# 填入 API Key 與商店序號
python mcp_server.py
```

## 工具清單

| 領域 | 工具名稱 | 說明 |
|------|---------|------|
| 訂單 | `get_order_list` | 訂單清單查詢（日期範圍最多7天） |
| 訂單 | `get_order_detail` | 訂單明細查詢（TGCode / TMCode） |
| 訂單 | `get_return_order_list` | 退貨單清單查詢 |
| 訂單 | `get_return_order_detail` | 退貨單明細查詢 |
| 訂單 | `get_exchange_order_list` | 換貨單清單查詢 |
| 商品 | `get_product_list` | 商品 SKU 清單查詢 |
| 商品 | `get_product_detail` | 商品完整明細查詢 |
| 商品 | `get_product_stock` | 商品庫存查詢 |
| 商品 | `get_shop_categories` | 商店自訂分類清單 |
| 商品 | `get_category_tree` | 系統商品分類樹狀查詢 |
| 商品 | `get_shop_payment_methods` | 商店付款方式清單 |
| 商品 | `get_shop_shipping_methods` | 商店配送方式清單 |
| 促銷 | `get_promotions` | 折扣活動清單查詢 |
| 促銷 | `get_promotion_detail` | 折扣活動明細查詢 |
| 促銷 | `get_promotion_salepages` | 折扣活動適用商品清單 |
| 物流 | `get_shipping_order` | 貨運單查詢（含 PII） |
| 物流 | `get_shipping_countries` | 配送國家清單查詢 |

## 環境變數

| 變數 | 必填 | 說明 |
|-----|------|------|
| `APP_91APP_API_KEY` | ✅ | 91APP OMNI 管理後台取得的 API Key |
| `APP_91APP_BASE_URL` | ✅ | API 基底 URL（如 `https://api.91app.com`） |
| `APP_91APP_SHOP_ID` | 建議填寫 | 預設商店序號（呼叫工具時可省略） |

## 架構說明

- 全部 91app Admin API 均使用 **POST** + JSON body，包含查詢操作
- 認證方式：HTTP Header `x-api-key`
- 回應格式：`{"Status": "Success"|"Error", "Data": ..., "ErrorMessage": ""}`
- `get_shipping_order` 與 `get_order_detail` 回傳含收件人個人資料（PII），請依法處理

## 測試

```bash
# 驗證連線
python scripts/auth/test_connection.py

# 執行所有工具測試
python tests/test_all_tools.py
```

## API 規格文件

- API 工具清單（含排除說明）：[`_spec/api-tools-list.md`](./_spec/api-tools-list.md)
- 機器可讀規格：[`_spec/tool-manifest.json`](./_spec/tool-manifest.json)
- 91app 官方文件：https://developer.91app.com/zh-tw/
