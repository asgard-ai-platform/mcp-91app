"""
IMS 通路版 Tools — 供 AI Agent 調用（Cat.11）

涵蓋：商品查詢、賣場檔、履約單、逆向履約單、提報單
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
# Tool 1: get_ims_channel_products — 商品資料查詢
# ============================================================
@mcp.tool()
def get_ims_channel_products(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢 IMS 通路版商品資料。回傳商品列表，含商品 ID、名稱、SKU 等。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_channel_products", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 2: get_ims_channel_salepages — 賣場檔清單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_salepages(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢 IMS 通路版賣場檔清單。回傳賣場檔列表，含 ID、名稱、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_channel_salepages", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 3: get_ims_channel_salepage — 單筆賣場檔查詢
# ============================================================
@mcp.tool()
def get_ims_channel_salepage(
    sale_page_id: str = Field(..., description="賣場檔 ID"),
) -> dict:
    """
    查詢 IMS 通路版單筆賣場檔明細。包含賣場檔名稱、商品、價格、狀態等。
    """
    result = api_get_ims("ims_channel_salepage", sale_page_id=sale_page_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 4: get_ims_channel_fulfillment_list — 履約單清單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_fulfillment_list(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
    status: Optional[str] = Field(default=None, description="履約狀態篩選"),
) -> dict:
    """
    查詢 IMS 通路版履約單清單。回傳履約單列表，含批次 ID、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    result = api_get_ims("ims_channel_fulfillment_list", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 5: get_ims_channel_fulfillment — 單筆履約單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_fulfillment(
    fulfillment_batch_id: str = Field(..., description="履約單批次 ID"),
) -> dict:
    """
    查詢 IMS 通路版單筆履約單明細。包含出貨品項、數量、物流資訊等。
    """
    result = api_get_ims("ims_channel_fulfillment", fulfillment_batch_id=fulfillment_batch_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 6: get_ims_channel_reverse_fulfillment_list — 逆向履約單清單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_reverse_fulfillment_list(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
    status: Optional[str] = Field(default=None, description="逆向履約狀態篩選"),
) -> dict:
    """
    查詢 IMS 通路版逆向履約單清單。逆向履約為退貨入庫流程。
    """
    params = {"page": page, "pageSize": page_size}
    if status:
        params["status"] = status
    result = api_get_ims("ims_channel_reverse_fulfillment_list", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 7: get_ims_channel_reverse_fulfillment — 單筆逆向履約單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_reverse_fulfillment(
    reverse_fulfillment_id: str = Field(..., description="逆向履約單 ID"),
) -> dict:
    """
    查詢 IMS 通路版單筆逆向履約單明細。包含退貨品項、入庫數量、狀態等。
    """
    result = api_get_ims("ims_channel_reverse_fulfillment", id=reverse_fulfillment_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 8: get_ims_channel_proposals — 提報單清單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_proposals(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢 IMS 通路版提報單清單。提報單為通路商向品牌提交的商品進貨/退貨申請。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_ims("ims_channel_proposals", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 9: get_ims_channel_proposal — 單筆提報單查詢
# ============================================================
@mcp.tool()
def get_ims_channel_proposal(
    proposal_id: str = Field(..., description="提報單 ID"),
) -> dict:
    """
    查詢 IMS 通路版單筆提報單明細。包含提報品項、數量、狀態、審核結果等。
    """
    result = api_get_ims("ims_channel_proposal", proposal_id=proposal_id)
    return extract_detail(result, key="data")
