"""
商品與庫存相關 Tools — 供 AI Agent 調用

涵蓋：商品 SKU 查詢、商品明細、庫存、商店分類、付款/配送方式、贈品、規格表、標籤
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
# Tool 1: get_product_list — 商品 SKU 清單
# ============================================================
@mcp.tool()
def get_product_list(
    start_date: str = Field(..., description="查詢起始日期，格式 yyyy-MM-dd"),
    end_date: str = Field(..., description="查詢結束日期"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    date_type: str = Field(default="CreateDateTime", description="日期類型：CreateDateTime / UpdateDateTime"),
    is_closed: Optional[bool] = Field(default=None, description="是否已下架：True=已下架 / False=上架中 / None=全部"),
    shop_category_id: Optional[int] = Field(default=None, description="商店分類 ID，不填取全部"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=200, description="每次回傳筆數，最多 200"),
) -> dict:
    """
    查詢商品（SalePage）SKU 清單。支援日期、上下架狀態、商店分類篩選。
    回傳 SKU 列表，含 SalePageId、商品名稱、SKU ID、售價、庫存等。
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
    if is_closed is not None:
        payload["IsClosed"] = is_closed
    if shop_category_id is not None:
        payload["ShopCategoryId"] = shop_category_id
    result = api_post("product_list", payload)
    return extract_list(result)


# ============================================================
# Tool 2: get_product_detail — 單一商品明細
# ============================================================
@mcp.tool()
def get_product_detail(
    sale_page_id: int = Field(..., description="商品（SalePage）序號，從 get_product_list 取得"),
) -> dict:
    """
    查詢單一商品完整明細。包含商品名稱、描述、規格、圖片、分類、價格等全部欄位。
    """
    payload = {"Id": sale_page_id}
    result = api_post("product_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 3: get_product_stock — 商品庫存查詢
# ============================================================
@mcp.tool()
def get_product_stock(
    sale_page_id: int = Field(..., description="商品（SalePage）序號"),
    sku_id: Optional[int] = Field(default=None, description="SKU 序號，不填則回傳所有 SKU 庫存"),
) -> dict:
    """
    查詢商品庫存。可查詢整個商品所有 SKU 的庫存，或指定單一 SKU 庫存。
    回傳 SKU 庫存數量列表。
    """
    payload: dict = {"Id": sale_page_id}
    if sku_id is not None:
        payload["SkuId"] = sku_id
    result = api_post("product_stock", payload)
    return extract_list(result)


# ============================================================
# Tool 4: get_shop_categories — 商店分類
# ============================================================
@mcp.tool()
def get_shop_categories(
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢商店的所有商店分類（店家自訂分類）。
    回傳樹型分類結構，含分類 ID、名稱、上層分類 ID 等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid}
    result = api_post("shop_categories", payload)
    return extract_list(result)


# ============================================================
# Tool 5: get_category_tree — 系統商品分類樹
# ============================================================
@mcp.tool()
def get_category_tree(
    source_category_id: Optional[int] = Field(default=None, description="上層系統分類 ID；不填則取根節點"),
) -> dict:
    """
    查詢 91app 系統商品分類樹狀結構（非商店自訂分類）。
    可從根節點往下遍歷，或指定特定分類節點取得子分類。
    """
    payload: dict = {}
    if source_category_id is not None:
        payload["SourceCategoryId"] = source_category_id
    result = api_post("category_tree", payload)
    return extract_list(result)


# ============================================================
# Tool 6: get_shop_payment_methods — 付款方式清單
# ============================================================
@mcp.tool()
def get_shop_payment_methods() -> dict:
    """
    查詢商店已啟用的付款方式清單（信用卡、ATM、貨到付款等）。
    不需傳入任何參數。
    """
    result = api_post("shop_payment_methods", {})
    return extract_list(result)


# ============================================================
# Tool 7: get_shop_shipping_methods — 配送方式清單
# ============================================================
@mcp.tool()
def get_shop_shipping_methods(
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢商店已啟用的配送方式清單（宅配、超商取貨、門市自取等）。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"Id": sid}
    result = api_post("shop_shipping_methods", payload)
    return extract_list(result)


# ============================================================
# Tool 8: get_shop_category_detail — 商品分類明細
# ============================================================
@mcp.tool()
def get_shop_category_detail(
    shop_category_id: int = Field(..., description="商店分類 ID，從 get_shop_categories 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢商品分類明細。包含分類名稱、排序、上層分類、圖片等詳細資訊。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "ShopCategoryId": shop_category_id}
    result = api_post("shop_category_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 9: get_gift_list — 贈品清單查詢
# ============================================================
@mcp.tool()
def get_gift_list(
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
    position: int = Field(default=0, ge=0, description="查詢起始位置（0-based）"),
    count: int = Field(default=50, ge=1, le=100, description="每次回傳筆數，最多 100"),
) -> dict:
    """
    查詢贈品清單。回傳商店內所有已建立的贈品列表。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Position": position, "Count": count}
    result = api_post("gift_list", payload)
    return extract_list(result)


# ============================================================
# Tool 10: get_gift_detail — 贈品明細查詢
# ============================================================
@mcp.tool()
def get_gift_detail(
    gift_id: int = Field(..., description="贈品 ID，從 get_gift_list 取得"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢單一贈品明細。包含贈品名稱、圖片、庫存、關聯商品等。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": gift_id}
    result = api_post("gift_detail", payload)
    return extract_detail(result)


# ============================================================
# Tool 11: get_gift_add_in_salepages — 贈品已加入商品頁查詢
# ============================================================
@mcp.tool()
def get_gift_add_in_salepages(
    gift_id: int = Field(..., description="贈品 ID"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢贈品已加入哪些商品頁。回傳關聯的 SalePage 列表。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "Id": gift_id}
    result = api_post("gift_add_in_salepages", payload)
    return extract_list(result)


# ============================================================
# Tool 12: get_gifts_by_salepage — 商品頁已加入贈品查詢
# ============================================================
@mcp.tool()
def get_gifts_by_salepage(
    sale_page_id: int = Field(..., description="商品頁 ID（SalePageId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢特定商品頁已加入的贈品清單。回傳該商品頁關聯的所有贈品。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "AddInSalePageId": sale_page_id}
    result = api_post("gifts_by_salepage", payload)
    return extract_list(result)


# ============================================================
# Tool 13: get_sale_product_tag — 商品頁標籤查詢
# ============================================================
@mcp.tool()
def get_sale_product_tag(
    sale_page_id: int = Field(..., description="商品頁 ID（SalePageId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    取得商品頁標籤。回傳該商品頁的所有標籤資訊。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "SalePageId": sale_page_id}
    result = api_post("sale_product_tag", payload)
    return extract_list(result)


# ============================================================
# Tool 14: get_spec_sheet — 商品頁規格表明細查詢
# ============================================================
@mcp.tool()
def get_spec_sheet(
    sale_page_id: int = Field(..., description="商品頁 ID（SalePageId）"),
    shop_id: Optional[int] = Field(default=None, description="商店序號，未填則使用環境變數 APP_91APP_SHOP_ID"),
) -> dict:
    """
    查詢商品頁規格表明細。回傳商品的詳細規格表資訊（如尺寸、材質等）。
    """
    sid = shop_id if shop_id is not None else settings.SHOP_ID
    payload = {"ShopId": sid, "SalePageId": sale_page_id}
    result = api_post("spec_sheet", payload)
    return extract_detail(result)
