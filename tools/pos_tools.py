"""
POS 相關 Tools — 供 AI Agent 調用（Cat.8）

涵蓋：POS 會員資料、優惠券、紅利點數、線下交易紀錄、POS 操作紀錄
注意：GetMemberInfo 回傳資料含會員 PII，請依隱私規範處理。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from pydantic import Field
from app import mcp
from tools.base_tool import api_post, extract_list, extract_detail
import config.settings as settings


# ============================================================
# Tool 1: get_pos_member_info — POS 會員基本資料查詢
# ============================================================
@mcp.tool()
def get_pos_member_info(
    cellphone: str = Field(..., description="會員手機號碼"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢 POS 會員基本資料。包含會員姓名、等級、生日、累計消費等。
    注意：回傳資料含會員 PII（個人資料），請依隱私規範處理。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Cellphone": cellphone}
    result = api_post("pos_member_info", payload)
    return extract_detail(result)


# ============================================================
# Tool 2: get_pos_member_coupon — POS 會員優惠券查詢
# ============================================================
@mcp.tool()
def get_pos_member_coupon(
    cellphone: str = Field(..., description="會員手機號碼"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢會員持有的優惠券清單。包含優惠券名稱、折扣類型、到期日等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Cellphone": cellphone}
    result = api_post("pos_member_coupon", payload)
    return extract_list(result)


# ============================================================
# Tool 3: get_pos_member_point — POS 會員紅利點數查詢
# ============================================================
@mcp.tool()
def get_pos_member_point(
    cellphone: str = Field(..., description="會員手機號碼"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢會員紅利點數。包含目前可用點數、即將到期點數等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Cellphone": cellphone}
    result = api_post("pos_member_point", payload)
    return extract_detail(result)


# ============================================================
# Tool 4: get_pos_order_list — 線下交易紀錄清單查詢
# ============================================================
@mcp.tool()
def get_pos_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢 POS 線下交易紀錄清單。支援日期範圍篩選。
    回傳線下交易列表，含交易序號、金額、門市、時間等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("pos_order_list", payload)
    return extract_list(result)


# ============================================================
# Tool 5: get_pos_order_summary — 線下交易紀錄資訊查詢
# ============================================================
@mcp.tool()
def get_pos_order_summary(
    pos_order_id: str = Field(..., description="POS 交易序號，從 get_pos_order_list 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆 POS 線下交易紀錄摘要。包含交易金額、品項、付款方式、門市資訊等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "POSOrderId": pos_order_id}
    result = api_post("pos_order_summary", payload)
    return extract_detail(result)


# ============================================================
# Tool 6: get_pos_actions — POS 機操作紀錄查詢
# ============================================================
@mcp.tool()
def get_pos_actions(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢 POS 機操作紀錄。包含各種 POS 操作（開單、核銷、退貨等）的紀錄。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("pos_actions", payload)
    return extract_list(result)
