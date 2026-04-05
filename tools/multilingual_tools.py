"""
內容多語系 Tools — 供 AI Agent 調用（Cat.7）

涵蓋：多語系內容查詢
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pydantic import Field
from app import mcp
from tools.base_tool import api_post, extract_detail


# ============================================================
# Tool 1: get_multilingual_content — 內容多語系查詢
# ============================================================
@mcp.tool()
def get_multilingual_content(
    content_type: str = Field(..., description="內容類型（如 SalePage / ShopCategory 等）"),
    content_id: int = Field(..., description="內容 ID（對應該類型的主鍵）"),
    language: str = Field(..., description="語系代碼（如 zh-TW / en-US / ja-JP）"),
) -> dict:
    """
    查詢指定內容的多語系翻譯資料。包含各語系翻譯欄位的內容。
    """
    payload = {
        "ContentType": content_type,
        "ContentId": content_id,
        "Language": language,
    }
    result = api_post("multilingual_content", payload)
    return extract_detail(result)
