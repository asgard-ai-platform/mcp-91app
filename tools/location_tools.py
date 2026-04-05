"""
門市相關 Tools — 供 AI Agent 調用（Cat.5）

涵蓋：門市推薦人查詢、店員幫手手機號碼查詢
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from pydantic import Field
from app import mcp
from tools.base_tool import api_post, extract_detail
import config.settings as settings


# ============================================================
# Tool 1: get_app_referee — 門市推薦人查詢
# ============================================================
@mcp.tool()
def get_app_referee(
    referee_id: str = Field(..., description="推薦人 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢門市推薦人資訊。包含推薦人名稱、門市、推薦碼等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "RefereeId": referee_id}
    result = api_post("app_referee", payload)
    return extract_detail(result)


# ============================================================
# Tool 2: get_frontline_cellphone — 店員幫手手機號碼查詢
# ============================================================
@mcp.tool()
def get_frontline_cellphone(
    member_id: str = Field(..., description="會員 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得店員幫手輸入的會員手機號碼。用於門市 POS 場景協助會員操作。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "MemberId": member_id}
    result = api_post("frontline_cellphone", payload)
    return extract_detail(result)
