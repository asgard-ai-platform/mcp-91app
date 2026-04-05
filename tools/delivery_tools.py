"""
配送相關 Tools — 供 AI Agent 調用

涵蓋：貨運單查詢、配送國家、境外物流、超商標籤列印、調貨單
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
# Tool 1: get_shipping_order — 貨運單查詢
# ============================================================
@mcp.tool()
def get_shipping_order(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    ts_code: Optional[str] = Field(default=None, description="訂單子單號（TSCode），不填則回傳該貨運單下所有訂單"),
) -> dict:
    """
    查詢特定貨運單（Shipping Order）的詳細資訊。
    包含配送狀態、物流商、收件人資訊（姓名、電話、地址）、預計到達日等。
    注意：回傳資料含收件人 PII（個人資料），請依隱私規範處理。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    if ts_code is not None:
        payload["TSCode"] = ts_code
    result = api_post("shipping_order", payload)
    return extract_detail(result)


# ============================================================
# Tool 2: get_shipping_countries — 配送國家清單
# ============================================================
@mcp.tool()
def get_shipping_countries(
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢商店已設定之配送方式的可配送國家清單。
    回傳支援的國家/地區清單，可用於確認海外訂單是否可配送。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid}
    result = api_post("shipping_countries", payload)
    return extract_list(result)


# ============================================================
# Tool 3: get_cross_border_shipping_invoices — 境外物流 Invoice 下載連結
# ============================================================
@mcp.tool()
def get_cross_border_shipping_invoices(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢境外物流出貨 Invoice 下載連結清單。
    適用於跨境電商需列印出貨 Invoice 的場景。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("cross_border_shipping_invoices", payload)
    return extract_list(result)


# ============================================================
# Tool 4: get_logistics_booking_note — 91APP 宅配託運單檔案
# ============================================================
@mcp.tool()
def get_logistics_booking_note(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得 91APP 物流中心宅配託運單檔案（PDF/標籤）。
    適用於使用 91APP 物流中心代理出貨的商家。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("logistics_booking_note", payload)
    return extract_detail(result)


# ============================================================
# Tool 5: get_logistics_return_shipping — 91APP 宅配退貨貨運歷程
# ============================================================
@mcp.tool()
def get_logistics_return_shipping(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢 91APP 物流中心宅配退貨的貨運歷程。
    回傳退貨物流追蹤資訊，包含各階段時間戳和狀態。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("logistics_return_shipping", payload)
    return extract_detail(result)


# ============================================================
# Tool 6: get_seven_eleven_label_pdf — 7-11 快速到店託運單
# ============================================================
@mcp.tool()
def get_seven_eleven_label_pdf(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得 7-11 快速到店託運單標籤 PDF。
    回傳標籤檔案下載連結或 Base64 內容。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("seven_eleven_label_pdf", payload)
    return extract_detail(result)


# ============================================================
# Tool 7: get_family_store_label — 全家超取標籤列印資訊
# ============================================================
@mcp.tool()
def get_family_store_label(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得全家便利商店超取標籤列印資訊。
    回傳標籤資料，含出貨人/收件人/包裹/門市等列印所需資訊。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("family_store_label", payload)
    return extract_detail(result)


# ============================================================
# Tool 8: get_family_store_freezer_label — 全家冷凍超取標籤列印資訊
# ============================================================
@mcp.tool()
def get_family_store_freezer_label(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得全家便利商店冷凍超取標籤列印資訊。
    專用於冷凍商品超取配送的標籤資料。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("family_store_freezer_label", payload)
    return extract_detail(result)


# ============================================================
# Tool 9: get_hilife_store_label — 萊爾富超取標籤列印資訊
# ============================================================
@mcp.tool()
def get_hilife_store_label(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得萊爾富便利商店超取標籤列印資訊。
    回傳標籤資料，含出貨人/收件人/包裹/門市等列印所需資訊。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("hilife_store_label", payload)
    return extract_detail(result)


# ============================================================
# Tool 10: get_okmart_store_label — OKmart 超取標籤列印資訊
# ============================================================
@mcp.tool()
def get_okmart_store_label(
    shipping_order_code: str = Field(..., description="貨運單配送編號（ShippingOrderCode）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得 OKmart 便利商店超取標籤列印資訊。
    回傳標籤資料，含出貨人/收件人/包裹/門市等列印所需資訊。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShippingOrderCode": shipping_order_code}
    result = api_post("okmart_store_label", payload)
    return extract_detail(result)


# ============================================================
# Tool 11: get_dispatch_order — 調貨單明細查詢
# ============================================================
@mcp.tool()
def get_dispatch_order(
    dispatch_order_id: str = Field(..., description="調貨單序號（DispatchOrderId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單筆調貨單明細。包含調貨來源/目的倉庫、商品、數量等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "DispatchOrderId": dispatch_order_id}
    result = api_post("dispatch_order", payload)
    return extract_detail(result)


# ============================================================
# Tool 12: get_dispatch_order_list — 調貨單清單查詢
# ============================================================
@mcp.tool()
def get_dispatch_order_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd 或 yyyy-MM-ddTHH:mm:ss"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢調貨單清單。支援日期範圍篩選。
    回傳調貨單列表，含調貨單序號、來源倉庫、目的倉庫、狀態等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {
        "ShopId": sid,
        "StartDate": start_date,
        "EndDate": end_date,
        "Position": position,
        "Count": count,
    }
    result = api_post("dispatch_order_list", payload)
    return extract_list(result)
