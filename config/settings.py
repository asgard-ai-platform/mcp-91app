"""91app Admin API 設定 — 支援 4 種認證方式"""
import os
import hashlib
import hmac
import time
import warnings


def _env_int(name: str, default: int = 0) -> int:
    """Parse an integer env var, tolerating unset or non-numeric values.

    Returns `default` when the variable is unset, empty, or non-numeric
    (e.g. an unexpanded `${VAR}` placeholder from an MCP host). This keeps
    the module importable when credentials are missing — tools that need a
    real SHOP_ID will surface the misconfiguration at API call time instead
    of taking down the whole MCP server at import. A non-numeric value emits
    a warning so misconfigurations remain visible.
    """
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        warnings.warn(
            f"{name} is set to non-numeric value {raw!r}; "
            f"falling back to {default}. "
            "Check for an unexpanded ${...} placeholder or a typo.",
            stacklevel=2,
        )
        return default


# ============================================================
# Auth Method 1: x-api-key（Cat.1-9 Admin API 核心）
# ============================================================
API_KEY = os.environ.get("APP_91APP_API_KEY", "")
BASE_URL = os.environ.get("APP_91APP_BASE_URL", "https://api.91app.com")
SHOP_ID = _env_int("APP_91APP_SHOP_ID")

# ============================================================
# Auth Method 2: n1-api-key（Cat.10-11 IMS, Cat.15 商品搜尋）
# ============================================================
N1_API_KEY = os.environ.get("APP_91APP_N1_API_KEY", "")
IMS_BASE_URL = os.environ.get("APP_91APP_IMS_BASE_URL", "https://ims-api.91app.com")

# ============================================================
# Auth Method 3: N1-API-KEY + HMAC-SHA256（Cat.12-13 金流）
# ============================================================
HMAC_SECRET = os.environ.get("APP_91APP_HMAC_SECRET", "")
PAYMENTS_BASE_URL = os.environ.get("APP_91APP_PAYMENTS_BASE_URL", "https://payments-api.91app.com")

# ============================================================
# Auth Method 4: ny-api-token / n1-api-key（Cat.14 會員 Connect Cloud）
# ============================================================
NY_API_TOKEN = os.environ.get("APP_91APP_NY_API_TOKEN", "")
MEMBER_BASE_URL = os.environ.get("APP_91APP_MEMBER_BASE_URL", "https://member-api.91app.com")

# ============================================================
# API 端點 — Cat.1-9（POST, x-api-key）
# ============================================================
ENDPOINTS = {
    # --- Cat.1 Order ---
    "order_list": "/ec/V2/SalesOrder/GetList",
    "order_detail": "/ec/V2/SalesOrder/Get",
    "order_shipping_processing_list": "/ec/V2/SalesOrder/GetShippingProcessingList",
    "return_order_list": "/ec/V2/ReturnGoodsOrder/GetList",
    "return_order_detail": "/ec/V2/ReturnGoodsOrder/Get",
    "exchange_order_list": "/ec/V2/ChangeGoodsOrder/GetList",
    "exchange_order_detail": "/ec/V2/ChangeGoodsOrder/Get",
    "recharge_receipt": "/ec/V2/RechargeReceipt/Get",
    "recharge_receipt_list": "/ec/V2/RechargeReceipt/GetList",
    "not_issue_invoice_order": "/ec/V2/NotIssueInvoiceSalesOrder/Get",
    "not_issue_invoice_order_list": "/ec/V2/NotIssueInvoiceSalesOrder/GetList",
    "regular_order_sequence": "/ec/V2/RegularOrder/GetRegularOrderSequence",
    "third_party_payment_info": "/ec/V2/ThirdPartyPayment/GetPaymentInfo",
    # --- Cat.2 Delivery ---
    "shipping_order": "/ec/V2/ShippingOrder/Get",
    "shipping_countries": "/ec/V2/Shop/GetShippingCountryList",
    "cross_border_shipping_invoices": "/ec/V2/CrossBorder/GetShippingInvoiceUrlList",
    "logistics_booking_note": "/ec/V2/LogisticsCenterAgent/GetBookingNote",
    "logistics_return_shipping": "/ec/V2/LogisticsCenterAgent/GetReturnShipping",
    "seven_eleven_label_pdf": "/ec/V2/SevenElevenTCat/GetLabelPdf",
    "family_store_label": "/ec/V2/Store/GetFamilyStoreLabelData",
    "family_store_freezer_label": "/ec/V2/Store/GetFamilyStoreForFreezerLabel",
    "hilife_store_label": "/ec/V2/Store/GetHiLifeStoreLabelData",
    "okmart_store_label": "/ec/V2/Store/GetOKmartStoreLabel",
    "dispatch_order": "/ec/V2/DispatchOrder/Get",
    "dispatch_order_list": "/ec/V2/DispatchOrder/GetList",
    # --- Cat.3 SalePage / Product ---
    "product_list": "/ec/V1/SalePage/GetSKUList",
    "product_detail": "/ec/V1/SalePage/GetMainDetail",
    "product_stock": "/ec/V1/SalePage/GetStock",
    "shop_categories": "/ec/V1/Category/GetShopCategory",
    "category_tree": "/ec/V1/Category/GetCategory",
    "shop_payment_methods": "/ec/V1/Shop/GetPayment",
    "shop_shipping_methods": "/ec/V1/Shop/GetShipping",
    "shop_category_detail": "/ec/V2/ShopCategory/GetShopCategoryDetail",
    "gift_detail": "/ec/V2/Gift/GetDetail",
    "gift_list": "/ec/V2/Gift/GetList",
    "gift_add_in_salepages": "/ec/V2/Gift/GetAddInSalePages",
    "gifts_by_salepage": "/ec/V2/Gift/GetGiftsByAddInSalePageId",
    "sale_product_tag": "/ec/V2/SaleProductTag/Get",
    "spec_sheet": "/ec/V2/SpecSheet/Get",
    # --- Cat.4 Promotion ---
    "promotions": "/ec/V2/Promotion/GetPromotions",
    "promotion_detail": "/ec/V2/Promotion/GetPromotionDetail",
    "promotion_salepages": "/ec/V2/Promotion/GetPromotionSalePages",
    "promotion_category_ids": "/ec/V2/Promotion/GetPromotionCategoryIdList",
    "promotion_addons_salepages": "/ec/V2/Promotion/GetPromotionAddOnsSalePages",
    "promotion_gifts": "/ec/V2/Promotion/GetPromotionGifts",
    "promotion_must_salepages": "/ec/V2/Promotion/GetPromotionMustSalePages",
    "promotion_registers": "/ec/V2/Promotion/GetPromotionRegisters",
    "custom_ranking_salepage": "/ec/V2/Promotion/GetCustomRankingSalePage",
    # --- Cat.5 Location ---
    "app_referee": "/ec/V2/AppReferee/Get",
    "frontline_cellphone": "/ec/V2/ThirdPartyMember/GetFrontlineCellphone",
    # --- Cat.7 Multilingual ---
    "multilingual_content": "/ec/V2/MultilingualContent/GetDetail",
    # --- Cat.8 POS ---
    "pos_member_info": "/pos/v1/GetMemberInfo",
    "pos_member_coupon": "/pos/v1/GetMemberOwnCoupon",
    "pos_member_point": "/pos/v1/GetMemberPoint",
    "pos_order_list": "/pos/v1/GetPOSOrderList",
    "pos_order_summary": "/pos/v1/GetPOSOrderSummary",
    "pos_actions": "/pos/v1/QueryPOSActions",
    # --- Cat.9 Invoice（與 Cat.1 不重複的端點）---
    "sales_order_final_list": "/ec/V2/SalesOrder/GetFinalList",
    "shipping_fail_fee_list": "/ec/V2/NotIssueInvoiceSalesOrder/GetShippingFailFeeList",
    "sales_order_fee_refund": "/ec/V2/RefundRequest/GetSalesOrderFeeRefund",
    "sales_order_fee_refund_list": "/ec/V2/RefundRequest/GetSalesOrderFeeRefundList",
    "sales_order_refund": "/ec/V2/RefundRequest/GetSalesOrderRefund",
    "sales_order_refund_list": "/ec/V2/RefundRequest/GetSalesOrderRefundList",
    "my_invoice_sales_order": "/ec/V2/MyInvoiceSalesOrder/Get",
}

# ============================================================
# IMS 端點 — Cat.10 Brand + Cat.11 Channel（GET, n1-api-key）
# ============================================================
IMS_BRAND_ENDPOINTS = {
    "ims_brand_orders": "/orders/list",
    "ims_brand_order": "/orders/{channel_type}/{order_code}",
    "ims_brand_fulfillment_list": "/fulfillment/list",
    "ims_brand_fulfillment": "/fulfillment/{fulfillment_batch_id}",
    "ims_brand_return_orders": "/return-orders/list",
    "ims_brand_return_order": "/return-orders/{channel_type}/{return_order_code}",
    "ims_brand_sku_available_qtys": "/stock-keeping-units/available-qtys",
    "ims_brand_warehouse_stocks": "/warehouse-stocks/{warehouse_id}/list",
    "ims_brand_warehouse_calculate_rule": "/warehouse-stocks/{warehouse_id}/calculate-rule",
    "ims_brand_warehouse_reserved_qtys": "/warehouse-stocks/{warehouse_id}/reserved-qtys",
    "ims_brand_warehouses": "/warehouses/list",
}

IMS_CHANNEL_ENDPOINTS = {
    "ims_channel_products": "/products",
    "ims_channel_salepages": "/salepages/list",
    "ims_channel_salepage": "/salepages/{sale_page_id}",
    "ims_channel_fulfillment_list": "/fulfillment/list",
    "ims_channel_fulfillment": "/fulfillment/{fulfillment_batch_id}",
    "ims_channel_reverse_fulfillment_list": "/reverse-fulfillment/list",
    "ims_channel_reverse_fulfillment": "/reverse-fulfillment/{id}",
    "ims_channel_proposals": "/proposals/list",
    "ims_channel_proposal": "/proposals/{proposal_id}",
}

# ============================================================
# Payments 端點 — Cat.12+13（GET/POST, HMAC）
# ============================================================
PAYMENTS_ENDPOINTS = {
    "payment_trade": "/v2/trades/{trade_id}",
    "payment_trade_record": "/v2/trades/{trade_id}/record",
    "stored_value_account": "/v2/stored-value/accounts/{id}",
    "stored_value_account_detail": "/v2/stored-value/accounts/{id}/detail",
    "stored_value_transactions": "/v2/stored-value/accounts/{id}/transactions",
    "stored_value_withdrawals": "/v2/stored-value/withdrawals",
    "stored_value_withdrawal_records": "/v2/stored-value/accounts/{id}/withdrawals/{code}/records",
    "verify_promotion_bin_code": "/v2/promotion-bin-code/verify-bin-code",
    "ledger_request": "/v2/ledgers/requests/{transfer_code}",
    "payment_methods": "/v2/payments/payment-methods",
    "payment_method_by_token": "/v2/payments/payment-methods/{binding_token}",
}

# ============================================================
# Member Connect Cloud 端點 — Cat.14（GET, ny-api-token）
# ============================================================
MEMBER_ENDPOINTS = {
    "members": "/v1/members/api/members",
    "query_members": "/v1/members/api/query-members",
    "tag_keys": "/v1/tags/api/batch-get-tag-keys",
    "tag_key": "/v1/tags/api/get-tag-key",
    "member_collections": "/v2/member-collections/query",
    "member_collections_cursor": "/v2/member-collections/query-by-cursor",
    "member_collection": "/v2/member-collections/{collection_id}",
    "member_collection_histories": "/v2/member-collections/{id}/histories",
}


# ============================================================
# Headers 函式 — 各認證方式
# ============================================================

def get_headers():
    """Cat.1-9: x-api-key 認證標頭"""
    if not API_KEY:
        raise RuntimeError(
            "APP_91APP_API_KEY environment variable is not set. "
            "Obtain the API key from the 91APP OMNI admin panel."
        )
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def get_headers_n1():
    """Cat.10-11, 15: n1-api-key 認證標頭"""
    if not N1_API_KEY:
        raise RuntimeError(
            "APP_91APP_N1_API_KEY environment variable is not set. "
            "Obtain the N1 API key from the 91APP IMS admin panel."
        )
    return {
        "n1-api-key": N1_API_KEY,
        "Content-Type": "application/json",
    }


def get_headers_hmac(body: str = ""):
    """Cat.12-13: N1-API-KEY + HMAC-SHA256 簽章標頭"""
    if not N1_API_KEY:
        raise RuntimeError(
            "APP_91APP_N1_API_KEY environment variable is not set."
        )
    if not HMAC_SECRET:
        raise RuntimeError(
            "APP_91APP_HMAC_SECRET environment variable is not set. "
            "Obtain the HMAC secret from the 91APP Payments admin panel."
        )
    timestamp = str(int(time.time()))
    message = f"{timestamp}{body}"
    signature = hmac.new(
        HMAC_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {
        "N1-API-KEY": N1_API_KEY,
        "N1-DATA-SIGNATURE": signature,
        "N1-TIMESTAMP": timestamp,
        "Content-Type": "application/json",
    }


def get_headers_member():
    """Cat.14: ny-api-token 認證標頭（fallback n1-api-key）"""
    token = NY_API_TOKEN or N1_API_KEY
    if not token:
        raise RuntimeError(
            "APP_91APP_NY_API_TOKEN or APP_91APP_N1_API_KEY environment variable is not set."
        )
    headers = {"Content-Type": "application/json"}
    if NY_API_TOKEN:
        headers["ny-api-token"] = NY_API_TOKEN
    else:
        headers["n1-api-key"] = N1_API_KEY
    return headers


# ============================================================
# URL 構建函式
# ============================================================

def get_url(endpoint_key):
    """Cat.1-9: 取得完整 API URL"""
    path = ENDPOINTS.get(endpoint_key, endpoint_key)
    return f"{BASE_URL.rstrip('/')}{path}"


def get_ims_url(endpoint_key, **path_params):
    """Cat.10-11: 取得 IMS API URL，支援路徑參數替換"""
    path = IMS_BRAND_ENDPOINTS.get(endpoint_key) or IMS_CHANNEL_ENDPOINTS.get(endpoint_key, endpoint_key)
    for k, v in path_params.items():
        path = path.replace(f"{{{k}}}", str(v))
    return f"{IMS_BASE_URL.rstrip('/')}{path}"


def get_payments_url(endpoint_key, **path_params):
    """Cat.12-13: 取得 Payments API URL"""
    path = PAYMENTS_ENDPOINTS.get(endpoint_key, endpoint_key)
    for k, v in path_params.items():
        path = path.replace(f"{{{k}}}", str(v))
    return f"{PAYMENTS_BASE_URL.rstrip('/')}{path}"


def get_member_url(endpoint_key, **path_params):
    """Cat.14: 取得 Member API URL"""
    path = MEMBER_ENDPOINTS.get(endpoint_key, endpoint_key)
    for k, v in path_params.items():
        path = path.replace(f"{{{k}}}", str(v))
    return f"{MEMBER_BASE_URL.rstrip('/')}{path}"
