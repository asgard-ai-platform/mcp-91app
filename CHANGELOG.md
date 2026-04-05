# Changelog

## [0.1.1] - 2026-04-01

### Changed
- 對齊 shopline reference repo 寫法（13 項偏離修正）
- `mcp_server.py`：加 shebang `#!/usr/bin/env python3`、docstring 改 zh-TW
- `config/settings.py`：加 module docstring、移除多餘 type hints
- `tools/base_tool.py`：docstring 改 zh-TW、`retries` 參數化
- 全部 `tools/*.py`：module docstring 改 zh-TW、加 `# ====` Tool 編號分隔線
- `pyproject.toml`：補 readme/license/authors/keywords/classifiers/urls、build backend 改 setuptools
- `.mcp.json`：格式對齊 shopline（`${PWD}`、加 `PYTHONPATH`）
- `CLAUDE.md`：全面改寫為 zh-TW、對齊 shopline 結構
- `tests/test_all_tools.py`：改 zh-TW、加 `asyncio.run(mcp.list_tools())` 工具數驗證
- `scripts/auth/test_connection.py`：改 zh-TW 輸出格式

### Added
- `.gitignore` — 與 shopline 一致
- `LICENSE` — MIT
- `CONTRIBUTING.md` — 91app 專屬貢獻指南

## [0.1.0] - 2026-04-01

### Added
- Initial release with 17 query-only tools
- **Order tools (5)**: `get_order_list`, `get_order_detail`, `get_return_order_list`, `get_return_order_detail`, `get_exchange_order_list`
- **Product tools (7)**: `get_product_list`, `get_product_detail`, `get_product_stock`, `get_shop_categories`, `get_category_tree`, `get_shop_payment_methods`, `get_shop_shipping_methods`
- **Promotion tools (3)**: `get_promotions`, `get_promotion_detail`, `get_promotion_salepages`
- **Delivery tools (2)**: `get_shipping_order`, `get_shipping_countries`
- `_spec/api-tools-list.md` — full API endpoint inventory with inclusion/exclusion rationale
- `_spec/tool-manifest.json` — machine-readable tool spec
- Connection test script: `scripts/auth/test_connection.py`
- Standalone test script: `tests/test_all_tools.py`

### Architecture
- All 91app Admin APIs use POST with JSON body (no HTTP GET)
- Authentication via `x-api-key` header
- Retry logic with exponential backoff (3 attempts, server errors only)
- PII note: `get_shipping_order` and `get_order_detail` return receiver personal data
