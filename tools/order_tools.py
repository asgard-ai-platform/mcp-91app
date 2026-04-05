"""
訂單相關 Tools — 供 AI Agent 調用

涵蓋：訂單查詢、退貨單查詢、換貨單查詢、補收單、載具資料、定期購、第三方付款
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
# Tool 1: get_order_list — 訂單清單查詢
# ============================================================
@mcp.tool()
def get_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    date_type: str = Field(default="OrderDateTime", description="日期類型：OrderDateTime（訂單成立）/ FinishDateTime（完成）/ UpdateDateTime（更新）"),
    order_status: Optional[str] = Field(default=None, description="訂單狀態：WaitingForPayment / WaitingForShipping / Shipping / Finish / Cancel"),
    order_deliver_type: Optional[str] = Field(default=None, description="配送方式：Home / StoreCashOnDelivery / StorePickup / LocationPickup 等"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢訂單清單。支援日期範圍（最多7天）、訂單狀態、配送方式篩選。
    回傳訂單摘要列表，含 TGCode、TMCode、TSCode、金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {
        "ShopId": sid,
        "DateType": date_type,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    if order_status:
        payload["OrderStatus"] = order_status
    if order_deliver_type:
        payload["OrderDeliverType"] = order_deliver_type

    result = api_post("order_list", payload)
    return extract_list(result)


# ============================================================
# Tool 2: get_order_detail — 單筆訂單明細
# ============================================================
@mcp.tool()
def get_order_detail(
    tg_code: Optional[str] = Field(default=None, description="訂單總單號 TGCode（與 tm_code 擇一必填）"),
    tm_code: Optional[str] = Field(default=None, description="訂單主單號 TMCode（與 tg_code 擇一必填）"),
    ts_code: Optional[str] = Field(default=None, description="訂單明細號 TSCode（可選，進一步篩選特定子單）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆訂單明細。需提供 TGCode 或 TMCode；可選填 TSCode 取得特定子單。
    回傳完整訂單資訊，含品項、金額、付款狀態、配送資訊等。
    """
    if not tg_code and not tm_code:
        return {"error": "tg_code 或 tm_code 至少需填一項", "code": 400}

    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {"ShopId": sid}
    if tg_code:
        payload["TGCode"] = tg_code
    if tm_code:
        payload["TMCode"] = tm_code
    if ts_code:
        payload["TSCode"] = ts_code

    result = api_post("order_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 3: get_return_order_list — 退貨單清單查詢
# ============================================================
@mcp.tool()
def get_return_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    date_type: str = Field(default="ReturnGoodDateTime", description="日期類型：ReturnGoodDateTime（退貨申請）/ UpdateDateTime（更新）"),
    return_status: Optional[str] = Field(default=None, description="退貨狀態：Processing / Finish / Cancel"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢退貨單清單。支援日期範圍（最多7天）與退貨狀態篩選。
    回傳退貨申請列表，含 ReturnGoodDetailId、原訂單號、退款金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {
        "ShopId": sid,
        "ReturnGoodDateType": date_type,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    if return_status:
        payload["ReturnGoodStatus"] = return_status

    result = api_post("return_order_list", payload)
    return extract_list(result)


# ============================================================
# Tool 4: get_return_order_detail — 單筆退貨單明細
# ============================================================
@mcp.tool()
def get_return_order_detail(
    return_good_detail_id: str = Field(..., description="退貨單明細序號（ReturnGoodDetailId），從 get_return_order_list 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆退貨單明細。需提供退貨單明細序號。
    回傳完整退貨資訊，含退貨商品、退款方式、處理狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "ReturnGoodDetailId": return_good_detail_id,
    }
    result = api_post("return_order_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 5: get_exchange_order_list — 換貨單清單查詢
# ============================================================
@mcp.tool()
def get_exchange_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    date_type: str = Field(default="ChangeGoodDateTime", description="日期類型：ChangeGoodDateTime（換貨申請）/ UpdateDateTime（更新）"),
    exchange_status: Optional[str] = Field(default=None, description="換貨狀態：Processing / Finish / Cancel"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢換貨單清單。支援日期範圍（最多7天）與換貨狀態篩選。
    回傳換貨申請列表，含 ChangeGoodDetailId、原訂單號、換貨商品、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {
        "ShopId": sid,
        "ChangeGoodDateType": date_type,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    if exchange_status:
        payload["ChangeGoodStatus"] = exchange_status

    result = api_post("exchange_order_list", payload)
    return extract_list(result)


# ============================================================
# Tool 6: get_exchange_order_detail — 單筆換貨單明細
# ============================================================
@mcp.tool()
def get_exchange_order_detail(
    change_good_detail_id: str = Field(..., description="換貨單明細序號（ChangeGoodDetailId），從 get_exchange_order_list 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆換貨單明細。包含換貨商品、退回方式、新出貨資訊等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ChangeGoodDetailId": change_good_detail_id}
    result = api_post("exchange_order_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 7: get_recharge_receipt — 補收單明細查詢
# ============================================================
@mcp.tool()
def get_recharge_receipt(
    recharge_receipt_id: str = Field(..., description="補收單序號（RechargeReceiptId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆補收單明細。包含補收金額、付款狀態、對應原訂單等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "RechargeReceiptId": recharge_receipt_id}
    result = api_post("recharge_receipt", payload)
    return extract_detail(result)


# ============================================================
# Tool 8: get_recharge_receipt_list — 補收單清單查詢
# ============================================================
@mcp.tool()
def get_recharge_receipt_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢補收單清單。支援日期範圍（最多7天）篩選。
    回傳補收單列表，含補收單序號、金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("recharge_receipt_list", payload)
    return extract_list(result)


# ============================================================
# Tool 9: get_not_issue_invoice_order — 訂單載具資料明細查詢
# ============================================================
@mcp.tool()
def get_not_issue_invoice_order(
    tg_code: str = Field(..., description="訂單總單號 TGCode"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢訂單載具資料明細（未開立發票的訂單資訊）。用於電子發票整合。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "TGCode": tg_code}
    result = api_post("not_issue_invoice_order", payload)
    return extract_detail(result)


# ============================================================
# Tool 10: get_not_issue_invoice_order_list — 訂單載具資料清單查詢
# ============================================================
@mcp.tool()
def get_not_issue_invoice_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢訂單載具資料清單。支援日期範圍篩選。
    回傳未開立發票的訂單載具清單，含 TGCode、載具類型等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("not_issue_invoice_order_list", payload)
    return extract_list(result)


# ============================================================
# Tool 11: get_shipping_processing_list — 出貨中訂單清單查詢
# ============================================================
@mcp.tool()
def get_shipping_processing_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期，最多與 start_date 相差 7 天"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢出貨處理中的訂單清單。可用於監控待出貨訂單。
    回傳正在出貨流程中的訂單摘要列表。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("order_shipping_processing_list", payload)
    return extract_list(result)


# ============================================================
# Tool 12: get_regular_order_sequence — 定期購訂單期數查詢
# ============================================================
@mcp.tool()
def get_regular_order_sequence(
    regular_order_id: str = Field(..., description="定期購訂單 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢定期購訂單的期數資訊。包含各期的出貨排程、金額、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "RegularOrderId": regular_order_id}
    result = api_post("regular_order_sequence", payload)
    return extract_detail(result)


# ============================================================
# Tool 13: get_third_party_payment_info — 第三方付款資訊查詢
# ============================================================
@mcp.tool()
def get_third_party_payment_info(
    tg_code: str = Field(..., description="訂單總單號 TGCode"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢訂單的第三方付款資訊。包含付款方式、交易序號、付款狀態等。
    適用於需要查詢線上支付（信用卡、ATM、超商代碼等）結果的場景。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "TGCode": tg_code}
    result = api_post("third_party_payment_info", payload)
    return extract_detail(result)
