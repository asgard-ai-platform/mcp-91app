# Contributing to MCP 91app

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork and clone the repository
2. Set up your environment:

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
cp .env.example .env
# Add your 91app API key and settings to .env
export APP_91APP_API_KEY=your_api_key_here
export APP_91APP_BASE_URL=https://api.91app.com
export APP_91APP_SHOP_ID=your_shop_id
```

3. Verify the setup:

```bash
python scripts/auth/test_connection.py
python tests/test_all_tools.py
```

## Adding a New Tool

1. Choose the appropriate module in `tools/` (or create a new `{domain}_tools.py`)
2. At the top of the module, import the `mcp` singleton and helpers:

```python
from app import mcp
from pydantic import Field
from typing import Optional
from tools.base_tool import api_post
import config.settings as settings
```

3. Define the tool with `@mcp.tool()`, typed parameters, `Field()` descriptions, and a docstring:

```python
# ============================================================
# Tool N: tool_name — 工具說明
# ============================================================
@mcp.tool()
def my_tool_name(
    param1: str = Field(description="說明（繁體中文）"),
    param2: Optional[int] = Field(default=None, description="說明"),
) -> dict:
    """工具的整體說明（繁體中文），成為 MCP tools/list 中的 description。"""
    sid = param2 if param2 is not None else settings.SHOP_ID
    payload = {"ShopId": sid, ...}
    result = api_post("endpoint_key", payload)
    if "error" in result:
        return result
    data = result.get("Data", [])
    items = data if isinstance(data, list) else [data]
    return {"data": items, "total": len(items)}
```

4. If you created a new module, import it in `mcp_server.py` to trigger registration:

```python
import tools.your_new_module  # noqa: F401
```

5. Add a test case in `tests/test_all_tools.py` (import and call the function directly)

No schema dict, no tool list, no extra wiring needed — `@mcp.tool()` handles registration automatically.

## Code Conventions

- **Language**: Code comments and tool descriptions are in Traditional Chinese (zh-Hant)
- **Dependencies**: `requests`, `mcp`, `pydantic` are the external dependencies. Avoid adding new ones unless absolutely necessary.
- **HTTP calls**: Use `api_post()` from `base_tool.py` — do not make raw HTTP calls in tools
- **Error handling**: Check `if "error" in result: return result` after every `api_post()` call
- **ShopId**: Default to `settings.SHOP_ID` when not provided by user

## Testing

All tests hit the live 91app Admin API and require valid credentials.

```bash
# Run the full E2E test suite
python tests/test_all_tools.py

# Test API connectivity
python scripts/auth/test_connection.py
```

Ensure all 17 tools pass before submitting a PR. If you added a new tool, include its test.
