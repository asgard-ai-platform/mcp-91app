"""
發票相關 Tools — 供 AI Agent 調用（Cat.9）

涵蓋：主單載具、運費退款、訂單退款、馬來西亞發票、運費發票載具
註：Cat.9 與 Cat.1 共用的端點（NotIssueInvoiceSalesOrder、ReturnGoodsOrder、RechargeReceipt）
    已在 order_tools.py 實作，此處僅包含 Cat.9 獨有的端點。
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
# Tool 1: get_sales_order_final_list — 主單載具資料清單查詢
# ============================================================
@mcp.tool()
def get_sales_order_final_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢主單載具資料清單。用於電子發票整合，取得已完成付款的訂單載具資訊。
    回傳載具資料列表，含訂單號、載具類型、載具資訊等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("sales_order_final_list", payload)
    return extract_list(result)


# ============================================================
# Tool 2: get_shipping_fail_fee_list — 逾期未取運費載具資料查詢
# ============================================================
@mcp.tool()
def get_shipping_fail_fee_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢逾期未取件導致需開立運費發票的載具資料。
    適用於超商取貨逾期退回後需另行開立運費發票的情境。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("shipping_fail_fee_list", payload)
    return extract_list(result)


# ============================================================
# Tool 3: get_sales_order_fee_refund — 運費退款單明細查詢
# ============================================================
@mcp.tool()
def get_sales_order_fee_refund(
    refund_request_id: str = Field(..., description="退款單序號（RefundRequestId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢運費退款單明細。包含退款金額、退款方式、處理狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "RefundRequestId": refund_request_id}
    result = api_post("sales_order_fee_refund", payload)
    return extract_detail(result)


# ============================================================
# Tool 4: get_sales_order_fee_refund_list — 運費退款單清單查詢
# ============================================================
@mcp.tool()
def get_sales_order_fee_refund_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢運費退款單清單。支援日期範圍篩選。
    回傳運費退款單列表，含退款單序號、金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("sales_order_fee_refund_list", payload)
    return extract_list(result)


# ============================================================
# Tool 5: get_sales_order_refund — 訂單退款單明細查詢（含運費）
# ============================================================
@mcp.tool()
def get_sales_order_refund(
    refund_request_id: str = Field(..., description="退款單序號（RefundRequestId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢訂單退款單明細（含運費）。包含商品退款金額、運費退款金額、退款方式等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "RefundRequestId": refund_request_id}
    result = api_post("sales_order_refund", payload)
    return extract_detail(result)


# ============================================================
# Tool 6: get_sales_order_refund_list — 訂單退款單清單查詢（含運費）
# ============================================================
@mcp.tool()
def get_sales_order_refund_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢訂單退款單清單（含運費）。支援日期範圍篩選。
    回傳退款單列表，含退款單序號、商品/運費退款金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("sales_order_refund_list", payload)
    return extract_list(result)


# ============================================================
# Tool 7: get_my_invoice_sales_order — 馬來西亞訂單發票明細查詢
# ============================================================
@mcp.tool()
def get_my_invoice_sales_order(
    tg_code: str = Field(..., description="訂單總單號 TGCode"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢馬來西亞訂單發票明細。適用於馬來西亞地區的發票查詢需求。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "TGCode": tg_code}
    result = api_post("my_invoice_sales_order", payload)
    return extract_detail(result)
