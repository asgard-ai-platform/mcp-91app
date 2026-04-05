# mcp-91app

MCP Server for **91app Admin API** — query-only tools for e-commerce operations.

**17 tools** covering orders, products, promotions, and delivery queries.

## Quick Start

```bash
cd mcp-servers/mcp-91app
pip install -e .
cp .env.example .env
# Fill in your 91app API key and shop ID
python mcp_server.py
```

## Available Tools

| Domain | Tool | Description |
|--------|------|-------------|
| Order | `get_order_list` | Query orders by date range (max 7 days) |
| Order | `get_order_detail` | Get full order details by TGCode/TMCode |
| Order | `get_return_order_list` | Query return order list |
| Order | `get_return_order_detail` | Get return order details |
| Order | `get_exchange_order_list` | Query exchange order list |
| Product | `get_product_list` | Query product SKU list |
| Product | `get_product_detail` | Get full product details |
| Product | `get_product_stock` | Query product stock levels |
| Product | `get_shop_categories` | Get shop custom categories |
| Product | `get_category_tree` | Get 91app system category tree |
| Product | `get_shop_payment_methods` | List payment methods |
| Product | `get_shop_shipping_methods` | List shipping methods |
| Promotion | `get_promotions` | Query promotions list |
| Promotion | `get_promotion_detail` | Get promotion full details |
| Promotion | `get_promotion_salepages` | Get products in a promotion |
| Delivery | `get_shipping_order` | Query shipping order details |
| Delivery | `get_shipping_countries` | List available shipping countries |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `APP_91APP_API_KEY` | ✅ | API key from 91APP OMNI admin panel |
| `APP_91APP_BASE_URL` | ✅ | e.g., `https://api.91app.com` |
| `APP_91APP_SHOP_ID` | Recommended | Default ShopId (used when not passed explicitly) |

## Architecture Notes

- All 91app Admin APIs use **POST** with JSON body — even read/query operations
- Auth: `x-api-key` header
- Response envelope: `{"Status": "Success"|"Error", "Data": ..., "ErrorMessage": ""}`
- `get_shipping_order` and `get_order_detail` return PII (receiver name, phone, address)

## Testing

```bash
# Verify connection
python scripts/auth/test_connection.py

# Run all tool tests
python tests/test_all_tools.py
```

## API Specification

- Full endpoint inventory: [`_spec/api-tools-list.md`](./_spec/api-tools-list.md)
- Machine-readable manifest: [`_spec/tool-manifest.json`](./_spec/tool-manifest.json)
- Official docs: https://developer.91app.com/zh-tw/
