"""
金流相關 Tools — 供 AI Agent 調用（Cat.12 + Cat.13）

涵蓋：交易查詢、儲值帳號、儲值金提領、BIN 碼驗證、帳務查詢、綁定支付方式
Auth: N1-API-KEY + N1-DATA-SIGNATURE（HMAC-SHA256）
註：Cat.13 的 4 個查詢端點與 Cat.12 StoredValue tag 完全重疊，不另建檔。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from pydantic import Field
from app import mcp
from tools.base_tool import api_get_payments, api_post_payments, extract_list, extract_detail


# ============================================================
# Tool 1: get_payment_trade — 交易查詢
# ============================================================
@mcp.tool()
def get_payment_trade(
    trade_id: str = Field(..., description="交易 ID"),
) -> dict:
    """
    查詢單筆交易資訊。包含交易金額、狀態、付款方式、建立時間等。
    """
    result = api_get_payments("payment_trade", trade_id=trade_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 2: get_payment_trade_record — 交易歷程查詢
# ============================================================
@mcp.tool()
def get_payment_trade_record(
    trade_id: str = Field(..., description="交易 ID"),
) -> dict:
    """
    查詢交易歷程紀錄。回傳該筆交易的所有狀態變更歷程。
    """
    result = api_get_payments("payment_trade_record", trade_id=trade_id)
    return extract_list(result, key="data")


# ============================================================
# Tool 3: get_stored_value_account — 儲值帳號查詢
# ============================================================
@mcp.tool()
def get_stored_value_account(
    account_id: str = Field(..., description="儲值帳號 ID"),
) -> dict:
    """
    查詢儲值帳號基本資訊。包含帳號餘額、狀態等。
    """
    result = api_get_payments("stored_value_account", id=account_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 4: get_stored_value_account_detail — 儲值帳號詳細資訊
# ============================================================
@mcp.tool()
def get_stored_value_account_detail(
    account_id: str = Field(..., description="儲值帳號 ID"),
) -> dict:
    """
    查詢儲值帳號詳細資訊。包含餘額明細、到期日、各類型儲值金分布等。
    """
    result = api_get_payments("stored_value_account_detail", id=account_id)
    return extract_detail(result, key="data")


# ============================================================
# Tool 5: get_stored_value_transactions — 儲值帳號交易紀錄
# ============================================================
@mcp.tool()
def get_stored_value_transactions(
    account_id: str = Field(..., description="儲值帳號 ID"),
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢儲值帳號的交易紀錄。包含儲值、扣款、退款等所有異動紀錄。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_payments("stored_value_transactions", params=params, id=account_id)
    return extract_list(result, key="data")


# ============================================================
# Tool 6: get_stored_value_withdrawals — 儲值金提領查詢
# ============================================================
@mcp.tool()
def get_stored_value_withdrawals(
    page: int = Field(default=1, ge=1, description="頁碼（1-based）"),
    page_size: int = Field(default=50, ge=1, le=100, description="每頁筆數，最多 100"),
) -> dict:
    """
    查詢儲值金提領清單。回傳所有儲值金提領申請，含提領金額、狀態等。
    """
    params = {"page": page, "pageSize": page_size}
    result = api_get_payments("stored_value_withdrawals", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 7: get_stored_value_withdrawal_records — 儲值金提領歷程
# ============================================================
@mcp.tool()
def get_stored_value_withdrawal_records(
    account_id: str = Field(..., description="儲值帳號 ID"),
    withdrawal_code: str = Field(..., description="提領編碼"),
) -> dict:
    """
    查詢儲值金提領歷程。回傳特定提領申請的狀態變更紀錄。
    """
    result = api_get_payments("stored_value_withdrawal_records", id=account_id, code=withdrawal_code)
    return extract_list(result, key="data")


# ============================================================
# Tool 8: verify_promotion_bin_code — BIN 碼驗證
# ============================================================
@mcp.tool()
def verify_promotion_bin_code(
    bin_code: str = Field(..., description="信用卡 BIN 碼（前 6-8 碼）"),
    promotion_id: str = Field(..., description="促銷活動 ID"),
) -> dict:
    """
    驗證信用卡 BIN 碼是否符合促銷活動條件。用於銀行卡優惠活動的資格驗證。
    """
    payload = {"binCode": bin_code, "promotionId": promotion_id}
    result = api_post_payments("verify_promotion_bin_code", payload)
    return extract_detail(result, key="data")


# ============================================================
# Tool 9: get_ledger_request — 帳務交易查詢
# ============================================================
@mcp.tool()
def get_ledger_request(
    transfer_code: str = Field(..., description="帳務交易轉帳碼"),
) -> dict:
    """
    查詢帳務交易資訊。包含轉帳金額、狀態、對象等。
    """
    result = api_get_payments("ledger_request", transfer_code=transfer_code)
    return extract_detail(result, key="data")


# ============================================================
# Tool 10: get_payment_methods — 查詢綁定支付方式（商店會員）
# ============================================================
@mcp.tool()
def get_payment_methods(
    member_id: Optional[str] = Field(default=None, description="會員 ID"),
) -> dict:
    """
    查詢商店會員的綁定支付方式清單。回傳信用卡/行動支付等已綁定的付款工具。
    """
    params = {}
    if member_id:
        params["memberId"] = member_id
    result = api_get_payments("payment_methods", params=params)
    return extract_list(result, key="data")


# ============================================================
# Tool 11: get_payment_method_by_token — 查詢綁定支付方式（Token）
# ============================================================
@mcp.tool()
def get_payment_method_by_token(
    binding_token: str = Field(..., description="綁定 Token"),
) -> dict:
    """
    透過綁定 Token 查詢綁定支付方式明細。包含卡號末四碼、到期日、類型等。
    """
    result = api_get_payments("payment_method_by_token", binding_token=binding_token)
    return extract_detail(result, key="data")
