"""
IMS 品牌版 Tools — 供 AI Agent 調用（Cat.10）

涵蓋：訂單查詢、履約單查詢、退貨單查詢、SKU 可賣量、倉庫庫存
Auth: n1-api-key ｜ REST-style GET
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from pydantic import Field
from app import mcp
from tools.base_tool import api_get_ims, extract_list, extract_detail


# ============================================================
# Tool 1: get_ims_brand_orders — IMS 品牌版訂單清單
# ============================================================
@mcp.tool()
def get_ims_brand_orders(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
    status: Optional[str] = Field(default=None, description="訂單狀態篩選"),
) -> dict:
    """
    查詢 IMS 品牌版訂單清單。回傳訂單列表，含訂單碼、通路、金額、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    result = api_get_ims("ims_brand_orders", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 2: get_ims_brand_order — IMS 品牌版單筆訂單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_order(
    channel_type: str = Field(..., description="通路類型（如 EC / POS）"),
    order_code: str = Field(..., description="訂單編碼"),
) -> dict:
    """
    查詢 IMS 品牌版單筆訂單明細。包含訂單品項、金額、通路、履約資訊等。
    """
    result = api_get_ims("ims_brand_order", channel_type=channel_type, order_code=order_code)
    return extract_detail(result, key="data")


# ============================================================
# Tool 3: get_ims_brand_fulfillment_list — 履約單清單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_fulfillment_list(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
    status: Optional[str] = Field(default=None, description="履約狀態篩選"),
) -> dict:
    """
    查詢 IMS 品牌版履約單清單。回傳履約單列表，含批次 ID、訂單號、倉庫、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    result = api_get_ims("ims_brand_fulfillment_list", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 4: get_ims_brand_fulfillment — 單筆履約單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_fulfillment(
    fulfillment_batch_id: str = Field(..., description="履約單批次 ID"),
) -> dict:
    """
    查詢 IMS 品牌版單筆履約單明細。包含出貨品項、數量、倉庫、物流資訊等。
    """
    result = api_get_ims("ims_brand_fulfillment", fulfillment_batch_id=fulfillment_batch_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 5: get_ims_brand_return_orders — 退貨單清單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_return_orders(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
    status: Optional[str] = Field(default=None, description="退貨狀態篩選"),
) -> dict:
    """
    查詢 IMS 品牌版退貨單清單。回傳退貨單列表，含退貨編碼、通路、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    result = api_get_ims("ims_brand_return_orders", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 6: get_ims_brand_return_order — 單筆退貨單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_return_order(
    channel_type: str = Field(..., description="通路類型（如 EC / POS）"),
    return_order_code: str = Field(..., description="退貨單編碼"),
) -> dict:
    """
    查詢 IMS 品牌版單筆退貨單明細。包含退貨品項、數量、退款金額等。
    """
    result = api_get_ims("ims_brand_return_order", channel_type=channel_type, return_order_code=return_order_code)
    return extract_detail(result, key="data")


# ============================================================
# Tool 7: get_ims_brand_sku_available_qtys — SKU 可賣量查詢
# ============================================================
@mcp.tool()
def get_ims_brand_sku_available_qtys(
    sku_ids: Optional[str] = Field(default=None, description="SKU ID 清單，逗號分隔（如 '123,456,789'）"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢 SKU 可賣量清單。回傳各 SKU 的可售數量、預約量等。
    """
    params = {"page": page, "pageSize": page_size}
    if sku_ids:
        params["skuIds"] = sku_ids
    result = api_get_ims("ims_brand_sku_available_qtys", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 8: get_ims_brand_warehouse_stocks — 倉庫庫存資料查詢
# ============================================================
@mcp.tool()
def get_ims_brand_warehouse_stocks(
    warehouse_id: str = Field(..., description="倉庫 ID"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢指定倉庫的庫存資料清單。回傳各 SKU 在該倉庫的庫存數量。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_brand_warehouse_stocks", params=params, warehouse_id=warehouse_id)
    return extract_list(result, key="data")


# ============================================================
# Tool 9: get_ims_brand_warehouse_calculate_rule — 倉庫庫存計算規則
# ============================================================
@mcp.tool()
def get_ims_brand_warehouse_calculate_rule(
    warehouse_id: str = Field(..., description="倉庫 ID"),
) -> dict:
    """
    取得倉庫庫存計算規則。回傳該倉庫的庫存計算方式（如 FIFO、安全庫存等設定）。
    """
    result = api_get_ims("ims_brand_warehouse_calculate_rule", warehouse_id=warehouse_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 10: get_ims_brand_warehouse_reserved_qtys — 倉庫庫存保留量查詢
# ============================================================
@mcp.tool()
def get_ims_brand_warehouse_reserved_qtys(
    warehouse_id: str = Field(..., description="倉庫 ID"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢倉庫庫存保留量。回傳各 SKU 因訂單保留的庫存數量。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_brand_warehouse_reserved_qtys", params=params, warehouse_id=warehouse_id)
    return extract_list(result, key="data")


# ============================================================
# Tool 11: get_ims_brand_warehouses — 倉庫清單查詢
# ============================================================
@mcp.tool()
def get_ims_brand_warehouses(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢 IMS 品牌版倉庫清單。回傳所有倉庫資訊，含倉庫 ID、名稱、地址等。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_brand_warehouses", params=params)
    return extract_list(result, key="data")
