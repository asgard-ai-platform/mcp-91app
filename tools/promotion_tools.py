"""
促銷活動相關 Tools — 供 AI Agent 調用

涵蓋：折扣活動查詢、活動明細、活動適用商品、加價購、贈品、必購、登記、排序
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
# Tool 1: get_promotions — 折扣活動清單
# ============================================================
@mcp.tool()
def get_promotions(
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    start_datetime: Optional[str] = Field(default=None, description="活動開始時間，格式 yyyy-MM-ddTHH:mm:ss"),
    end_datetime: Optional[str] = Field(default=None, description="活動結束時間"),
    date_time_type: Optional[str] = Field(default=None, description="時間篩選類型：StartDateTime / EndDateTime / UpdateDateTime"),
    status: Optional[list] = Field(default=None, description="活動狀態清單：Active（進行中）/ Inactive（未開始）/ Expired（已結束）"),
    promotion_type: Optional[str] = Field(default=None, description="活動類型代碼（如 Discount / GiftWithPurchase 等）"),
    promotion_id: Optional[int] = Field(default=None, description="指定折扣活動 ID"),
) -> dict:
    """
    查詢折扣活動清單。支援依時間範圍、狀態、活動類型篩選。
    回傳活動列表，含活動 ID、名稱、類型、時間範圍、狀態等。單次最多 1000 筆。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {"ShopId": sid}
    if start_datetime:
        payload["StartDateTime"] = start_datetime
    if end_datetime:
        payload["EndDateTime"] = end_datetime
    if date_time_type:
        payload["DateTimeType"] = date_time_type
    if status:
        payload["Status"] = status
    if promotion_type:
        payload["PromotionTypeDef"] = promotion_type
    if promotion_id is not None:
        payload["PromotionId"] = promotion_id
    result = api_post("promotions", payload)
    return extract_list(result)


# ============================================================
# Tool 2: get_promotion_detail — 單一活動明細
# ============================================================
@mcp.tool()
def get_promotion_detail(
    promotion_id: int = Field(..., description="折扣活動 ID，從 get_promotions 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單一折扣活動完整明細。包含活動規則、門檻設定、套用範圍、贈品設定等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("promotion_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 3: get_promotion_salepages — 活動適用商品
# ============================================================
@mcp.tool()
def get_promotion_salepages(
    promotion_id: int = Field(..., description="折扣活動 ID，從 get_promotions 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    tag: Optional[str] = Field(default=None, description="區塊標籤（用於紅配綠活動指定區塊，如 'Red' / 'Green'）"),
) -> dict:
    """
    查詢折扣活動的適用商品清單（SalePage 列表）。
    回傳活動中包含的所有商品頁面，含 SalePageId、商品名稱等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload: dict = {"ShopId": sid, "Id": promotion_id}
    if tag:
        payload["Tag"] = tag
    result = api_post("promotion_salepages", payload)
    return extract_list(result)


# ============================================================
# Tool 4: get_promotion_category_ids — 活動商品分類清單
# ============================================================
@mcp.tool()
def get_promotion_category_ids(
    promotion_id: int = Field(..., description="折扣活動 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢折扣活動的適用商品分類 ID 清單。
    回傳活動中包含的所有商品分類 ID。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("promotion_category_ids", payload)
    return extract_list(result)


# ============================================================
# Tool 5: get_promotion_addons_salepages — 加價購商品清單
# ============================================================
@mcp.tool()
def get_promotion_addons_salepages(
    promotion_id: int = Field(..., description="折扣活動 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢折扣活動的加價購商品清單。
    回傳活動中設定的加價購商品列表，含加價金額、商品資訊等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("promotion_addons_salepages", payload)
    return extract_list(result)


# ============================================================
# Tool 6: get_promotion_gifts — 活動贈品查詢
# ============================================================
@mcp.tool()
def get_promotion_gifts(
    promotion_id: int = Field(..., description="折扣活動 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢折扣活動的贈品清單。回傳活動設定的所有贈品，含贈品名稱、數量等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("promotion_gifts", payload)
    return extract_list(result)


# ============================================================
# Tool 7: get_promotion_must_salepages — 必購商品清單
# ============================================================
@mcp.tool()
def get_promotion_must_salepages(
    promotion_id: int = Field(..., description="折扣活動 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢折扣活動的必購商品清單。活動需購買指定必購商品才能觸發優惠。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("promotion_must_salepages", payload)
    return extract_list(result)


# ============================================================
# Tool 8: get_promotion_registers — 登記活動名單查詢
# ============================================================
@mcp.tool()
def get_promotion_registers(
    promotion_id: int = Field(..., description="折扣活動 ID（限登記型活動）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢登記型折扣活動的登記名單。含登記會員、登記時間等資訊。
    注意：回傳資料可能含會員 PII，請依隱私規範處理。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id, "Position": position, "Count": count}
    result = api_post("promotion_registers", payload)
    return extract_list(result)


# ============================================================
# Tool 9: get_custom_ranking_salepage — 活動商品排序查詢
# ============================================================
@mcp.tool()
def get_custom_ranking_salepage(
    promotion_id: int = Field(..., description="折扣活動 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢折扣活動的商品自訂排序。回傳活動內商品的顯示排序設定。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": promotion_id}
    result = api_post("custom_ranking_salepage", payload)
    return extract_list(result)
