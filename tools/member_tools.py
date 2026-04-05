"""
會員 Connect Cloud Tools — 供 AI Agent 調用（Cat.14）

涵蓋：會員查詢、標籤查詢、客群查詢
Auth: ny-api-token / n1-api-key ｜ REST-style GET
注意：會員查詢回傳資料含 PII（個人資料），請依隱私規範處理。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from pydantic import Field
from app import mcp
from tools.base_tool import api_get_member, extract_list, extract_detail


# ============================================================
# Tool 1: get_members — 會員查詢
# ============================================================
@mcp.tool()
def get_members(
    cellphone: Optional[str] = Field(default=None, description="會員手機號碼"),
    email: Optional[str] = Field(default=None, description="會員電子郵件"),
    member_id: Optional[str] = Field(default=None, description="會員 ID"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢會員資料。支援手機、郵件、會員 ID 篩選。
    注意：回傳資料含會員 PII（個人資料），請依隱私規範處理。
    """
    params = {"page": page, "pageSize": page_size}
    if cellphone:
        params["cellphone"] = cellphone
    if email:
        params["email"] = email
    if member_id:
        params["memberId"] = member_id
    result = api_get_member("members", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 2: query_members — 會員篩選
# ============================================================
@mcp.tool()
def query_members(
    query: Optional[str] = Field(default=None, description="篩選條件（如會員等級、註冊日期範圍）"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    進階會員篩選查詢。支援多條件組合篩選。
    注意：回傳資料含會員 PII（個人資料），請依隱私規範處理。
    """
    params = {"page": page, "pageSize": page_size}
    if query:
        params["query"] = query
    result = api_get_member("query_members", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 3: get_tag_keys — 查詢標籤群組內標籤
# ============================================================
@mcp.tool()
def get_tag_keys(
    tag_group_ids: Optional[str] = Field(default=None, description="標籤群組 ID 清單，逗號分隔"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    批次查詢標籤群組內的標籤。回傳標籤 ID、名稱、群組歸屬等。
    """
    params = {"page": page, "pageSize": page_size}
    if tag_group_ids:
        params["tagGroupIds"] = tag_group_ids
    result = api_get_member("tag_keys", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 4: get_tag_key — 標籤查詢
# ============================================================
@mcp.tool()
def get_tag_key(
    tag_key_id: str = Field(..., description="標籤 ID"),
) -> dict:
    """
    查詢單一標籤詳細資訊。包含標籤名稱、類型、描述等。
    """
    params = {"tagKeyId": tag_key_id}
    result = api_get_member("tag_key", params=params)
    return extract_detail(result, key="data")


# ============================================================
# Tool 5: get_member_collections — 客群清單查詢（offset）
# ============================================================
@mcp.tool()
def get_member_collections(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    取得客群清單（offset 分頁）。回傳客群列表，含客群 ID、名稱、會員數等。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_member("member_collections", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 6: get_member_collections_cursor — 客群清單查詢（cursor）
# ============================================================
@mcp.tool()
def get_member_collections_cursor(
    cursor: Optional[str] = Field(default=None, description="游標值，從上次回應的 nextCursor 取得"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    取得客群清單（cursor 分頁）。適用於大量資料的遍歷場景。
    """
    params = {"pageSize": page_size}
    if cursor:
        params["cursor"] = cursor
    result = api_get_member("member_collections_cursor", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 7: get_member_collection — 單一客群資料查詢
# ============================================================
@mcp.tool()
def get_member_collection(
    collection_id: str = Field(..., description="客群 ID"),
) -> dict:
    """
    查詢單一客群資料。包含客群名稱、條件規則、會員數、建立者等。
    """
    result = api_get_member("member_collection", collection_id=collection_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 8: get_member_collection_histories — 客群異動歷程
# ============================================================
@mcp.tool()
def get_member_collection_histories(
    collection_id: str = Field(..., description="客群 ID"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    取得客群異動歷程。回傳客群條件/成員的變更紀錄。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_member("member_collection_histories", params=params, id=collection_id)
    return extract_list(result, key="data")
