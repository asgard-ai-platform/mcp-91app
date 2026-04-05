# 91app Admin API — 完整端點盤點

> 建立日期：2025-07 ｜ 最後更新：2025-07
> 資料來源：developer.91app.com Swagger/OpenAPI specs（透過 Docusaurus bundle 解析）
> 範圍：16 個公開 API 分類（230+ 端點）+ 5 個隱藏/403 分類
> 已實作工具：17 個（query-only）

---

## 分類總覽

| # | Slug | 中文名稱 | API 版本 | 認證方式 | 端點數 | 查詢 | 寫入 | 狀態 |
|---|------|---------|---------|---------|--------|------|------|------|
| 1 | admin-order | 訂單 | v1.0.0 | x-api-key | 16 | 13 | 3 | ✅ 公開 |
| 2 | admin-delivery | 物流/出貨 | v1.0.0 | x-api-key | 34 | 12 | 22 | ✅ 公開 |
| 3 | admin-salepage | 商品頁 | v1.0.0 | x-api-key | 24 | 12 | 12 | ✅ 公開 |
| 4 | admin-promotion | 折扣活動 | v1.0.0 | x-api-key | 20 | 9 | 11 | ✅ 公開 |
| 5 | admin-location | 門市 | v1.0.0 | x-api-key | 5 | 2 | 3 | ✅ 公開 |
| 6 | admin-member-tier | 會員等級 | v1.0.0 | x-api-key | 1 | 0 | 1 | ✅ 公開 |
| 7 | admin-multilingual-content | 內容多語系 | v1.0.0 | x-api-key | 2 | 1 | 1 | ✅ 公開 |
| 8 | admin-pos | POS | v1.0.0 | x-api-key | 12 | 6 | 6 | ✅ 公開 |
| 9 | admin-invoice | 發票 | v1.0.0 | x-api-key | 13 | 13 | 0 | ✅ 公開 |
| 10 | admin-ims-brand | IMS 品牌版 | v0.9.15 | n1-api-key | 26 | 11 | 15 | ✅ 公開 |
| 11 | admin-ims-channel | IMS 通路版 | v0.9.11 | n1-api-key | 21 | 9 | 12 | ✅ 公開 |
| 12 | admin-payments | 金流 | v2.0.0 | N1-API-KEY + HMAC | 30 | 11 | 18+1cb | ✅ 公開 |
| 13 | admin-payments-stored-value | 儲值中心 POS | preview | N1-API-KEY + HMAC | 10 | 4 | 5+1cb | ✅ 公開 |
| 14 | admin-member | 會員 Connect Cloud | v1.0.0 | ny-api-token / n1-api-key | 21 | 8 | 13 | ✅ 公開 |
| 15 | admin-salepage-search | 商品頁搜尋 | v0.0.0 | n1-api-key | 1 | 0 | 1 | ✅ 公開 |
| 16 | admin-data-sync-webhook | DataSync Webhook | v1.0.0 | (商家實作) | 1 | 0 | 0+1cb | ✅ 公開 |
| — | admin-member-hidden | 會員（隱藏） | — | x-api-key + ny-api-token | ? | — | — | 🔒 403 |
| — | admin-ims-hidden | IMS（隱藏） | — | — | ? | — | — | 🔒 403 |
| — | admin-data-sync-hidden | Data Sync（隱藏） | — | — | ? | — | — | 🔒 403 |
| — | admin-express-checkout-hidden | 快速結帳（隱藏） | — | — | ? | — | — | 🔒 403 |
| — | admin-payments-module | 金流模組（隱藏） | — | — | ? | — | — | 🔒 403 |

**統計（16 個公開分類）**：

| 指標 | 數量 |
|------|------|
| 端點總數 | 237 |
| 查詢（Read） | 111 |
| 寫入（Write） | 123 |
| Callback/Webhook | 3 |
| **已實作工具** | **17**（全部為 query-only） |

**認證方式分布**：
- `x-api-key`：Categories 1-9（Admin API 核心）
- `n1-api-key`：Categories 10-11, 15（IMS + 商品搜尋）
- `N1-API-KEY` + `N1-DATA-SIGNATURE`（HMAC-SHA256）：Categories 12-13（金流）
- `ny-api-token` / `n1-api-key`：Category 14（會員 Connect Cloud）

**重複端點注意**：Invoice (Cat.9) 與 Order (Cat.1) 共用部分端點（NotIssueInvoiceSalesOrder、ReturnGoodsOrder、RechargeReceipt）。Payments Stored Value (Cat.13) 與 Payments (Cat.12) StoredValue tag 有大量重疊。

**隱藏分類推測**：使用者截圖的 18 項中第 12-18 項（外部LINE綁定、門市店員、即時給點回收、外部異動會員個資、外部加入會員、推薦人綁定、推薦人報表）推測屬於 `admin-member-hidden` 分類下的子功能。其中「推薦人」和「門市店員」端點已出現在 `admin-location` spec 中。

---

## Cat.1 Order 訂單（16 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 13 Query + 3 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/SalesOrder/GetList` | 訂單清單查詢 | 🔍 | ✅ `get_order_list` |
| 2 | `/ec/V2/SalesOrder/Get` | 訂單查詢 | 🔍 | ✅ `get_order_detail` |
| 3 | `/ec/V2/SalesOrder/GetShippingProcessingList` | 出貨中訂單清單查詢 | 🔍 | ⏳ `get_order_list` 可替代 |
| 4 | `/ec/V2/ReturnGoodsOrder/GetList` | 退貨清單查詢 | 🔍 | ✅ `get_return_order_list` |
| 5 | `/ec/V2/ReturnGoodsOrder/Get` | 退貨單查詢 | 🔍 | ✅ `get_return_order_detail` |
| 6 | `/ec/V2/RechargeReceipt/Get` | 補收單明細查詢 | 🔍 | ⏳ |
| 7 | `/ec/V2/RechargeReceipt/GetList` | 補收單清單查詢 | 🔍 | ⏳ |
| 8 | `/ec/V2/ChangeGoodsOrder/GetList` | 換貨清單查詢 | 🔍 | ✅ `get_exchange_order_list` |
| 9 | `/ec/V2/ChangeGoodsOrder/Get` | 換貨單查詢 | 🔍 | ⏳ |
| 10 | `/ec/V2/NotIssueInvoiceSalesOrder/GetList` | 訂單載具資料清單查詢 | 🔍 | ⏳ |
| 11 | `/ec/V2/NotIssueInvoiceSalesOrder/Get` | 訂單載具資料明細查詢 | 🔍 | ⏳ |
| 12 | `/ec/V2/RegularOrder/GetRegularOrderSequence` | 定期購訂單期數查詢 | 🔍 | ⏳ |
| 13 | `/ec/V2/ThirdPartyPayment/GetPaymentInfo` | 第三方付款資訊查詢 | 🔍 | ⏳ |
| 14 | `/ec/V2/ReturnGoodsOrder/ReturnProcess` | 退貨處理 | ✏️ | ⛔ |
| 15 | `/ec/V2/RechargeReceipt/Create` | 建立補收單 | ✏️ | ⛔ |
| 16 | `/ec/V2/SalesOrder/Cancel` | 取消訂單 | ✏️ | ⛔ |

---

## Cat.2 Delivery 物流/出貨（34 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 12 Query + 22 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/ShippingOrder/Get` | 貨運單查詢 | 🔍 | ✅ `get_shipping_order` |
| 2 | `/ec/V2/Shop/GetShippingCountryList` | 配送國家清單查詢 | 🔍 | ✅ `get_shipping_countries` |
| 3 | `/ec/V2/CrossBorder/GetShippingInvoiceUrlList` | 境外物流 Invoice 下載連結 | 🔍 | ⏳ |
| 4 | `/ec/V2/LogisticsCenterAgent/GetBookingNote` | 91APP 宅配託運單檔案 | 🔍 | ⏳ |
| 5 | `/ec/V2/LogisticsCenterAgent/GetReturnShipping` | 91APP 宅配退貨貨運歷程 | 🔍 | ⏳ |
| 6 | `/ec/V2/SevenElevenTCat/GetLabelPdf` | 7-11 快速到店託運單 | 🔍 | ⏳ |
| 7 | `/ec/V2/Store/GetFamilyStoreLabelData` | 全家超取標籤列印資訊 | 🔍 | ⏳ |
| 8 | `/ec/V2/Store/GetFamilyStoreForFreezerLabel` | 全家冷凍超取標籤列印資訊 | 🔍 | ⏳ |
| 9 | `/ec/V2/Store/GetHiLifeStoreLabelData` | 萊爾富超取標籤列印資訊 | 🔍 | ⏳ |
| 10 | `/ec/V2/Store/GetOKmartStoreLabel` | OKmart 超取標籤列印 | 🔍 | ⏳ |
| 11 | `/ec/V2/DispatchOrder/Get` | 調貨單明細查詢 | 🔍 | ⏳ |
| 12 | `/ec/V2/DispatchOrder/GetList` | 調貨單清單查詢 | 🔍 | ⏳ |
| 13–34 | *(22 個寫入端點)* | 門市自取/宅配/超取/境外/數位發送配號、出貨確認、取消配號等 | ✏️ | ⛔ |

---

## Cat.3 SalePage 商品頁（24 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 12 Query + 12 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V1/SalePage/GetStock` | 商品即時庫存查詢 | 🔍 | ✅ `get_product_stock` |
| 2 | `/ec/V1/Category/GetCategory` | 商品品類查詢 | 🔍 | ✅ `get_category_tree` |
| 3 | `/ec/V1/Category/GetShopCategory` | 商品分類查詢 | 🔍 | ✅ `get_shop_categories` |
| 4 | `/ec/V1/SalePage/GetMain` | 商品頁內容查詢 | 🔍 | ⏳ `GetMainDetail` 更完整 |
| 5 | `/ec/V1/Shop/GetShipping` | 查詢商店支援物流方式 | 🔍 | ✅ `get_shop_shipping_methods` |
| 6 | `/ec/V2/ShopCategory/GetShopCategoryDetail` | 查詢商品分類明細 | 🔍 | ⏳ |
| 7 | `/ec/V2/Gift/GetDetail` | 贈品明細查詢 | 🔍 | ⏳ |
| 8 | `/ec/V2/Gift/GetList` | 贈品清單查詢 | 🔍 | ⏳ |
| 9 | `/ec/V2/Gift/GetAddInSalePages` | 贈品已加入商品頁查詢 | 🔍 | ⏳ |
| 10 | `/ec/V2/Gift/GetGiftsByAddInSalePageId` | 商品頁已加入贈品查詢 | 🔍 | ⏳ |
| 11 | `/ec/V2/SaleProductTag/Get` | 取得商品頁標籤 | 🔍 | ⏳ |
| 12 | `/ec/V2/SpecSheet/Get` | 查詢商品頁規格表明細 | 🔍 | ⏳ |
| 13–24 | *(12 個寫入端點)* | 庫存變更、商品新增刪除、贈品管理、品牌關聯、規格表刪除等 | ✏️ | ⛔ |

**註**：現有工具 `get_product_list` (`GetSKUList`)、`get_product_detail` (`GetMainDetail`)、`get_shop_payment_methods` (`GetPayment`) 為 V1 legacy 端點，未列入 Swagger 但確認可用。

---

## Cat.4 Promotion 折扣活動（20 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 9 Query + 11 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/Promotion/GetPromotions` | 折扣活動清單查詢 | 🔍 | ✅ `get_promotions` |
| 2 | `/ec/V2/Promotion/GetPromotionDetail` | 折扣活動明細查詢 | 🔍 | ✅ `get_promotion_detail` |
| 3 | `/ec/V2/Promotion/GetPromotionSalePages` | 折扣活動商品清單查詢 | 🔍 | ✅ `get_promotion_salepages` |
| 4 | `/ec/V2/Promotion/GetPromotionCategoryIdList` | 折扣活動商品分類清單查詢 | 🔍 | ⏳ |
| 5 | `/ec/V2/Promotion/GetPromotionAddOnsSalePages` | 加價購商品表清單查詢 | 🔍 | ⏳ |
| 6 | `/ec/V2/Promotion/GetPromotionGifts` | 折扣活動贈品查詢 | 🔍 | ⏳ |
| 7 | `/ec/V2/Promotion/GetPromotionMustSalePages` | 折扣活動必購商品清單查詢 | 🔍 | ⏳ |
| 8 | `/ec/V2/Promotion/GetPromotionRegisters` | 登記活動登記名單查詢 | 🔍 | ⏳ 含 PII |
| 9 | `/ec/V2/Promotion/GetCustomRankingSalePage` | 折扣活動商品排序查詢 | 🔍 | ⏳ |
| 10–20 | *(11 個寫入端點)* | 新增/刪除/更新活動、商品表/分類異動、圖片上傳等 | ✏️ | ⛔ |

---

## Cat.5 Location 門市（5 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 2 Query + 3 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/AppReferee/Get` | 門市推薦人查詢 | 🔍 | ⏳ 通用性低 |
| 2 | `/ec/V2/ThirdPartyMember/GetFrontlineCellphone` | 取得店員幫手輸入手機號碼 | 🔍 | ⏳ 特殊場景 |
| 3 | `/ec/V1/Location/CreateSMSLocation` | 新增門市資訊 | ✏️ | ⛔ |
| 4 | `/ec/V1/Location/DeleteSMSLocation` | 刪除門市資訊 | ✏️ | ⛔ |
| 5 | `/ec/V1/Location/UpdateSMSLocation` | 修改門市資訊 | ✏️ | ⛔ |

---

## Cat.6 Member Tier 會員等級（1 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 0 Query + 1 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/MemberTier/UpdateMemberTierInfo` | 更新會員等級資料 | ✏️ | ⛔ |

---

## Cat.7 Multilingual Content 內容多語系（2 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 1 Query + 1 Write

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/ec/V2/MultilingualContent/GetDetail` | 內容多語系查詢 | 🔍 | ⏳ |
| 2 | `/ec/V2/MultilingualContent/InsertOrUpdate` | 內容多語系異動 | ✏️ | ⛔ |

---

## Cat.8 POS（12 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 6 Query + 6 Write ｜ 含 PII（會員資料、紅利、優惠券）

| # | Path | 名稱 | 類型 | 狀態 |
|---|------|------|------|------|
| 1 | `/pos/v1/GetMemberInfo` | 查詢會員基本資料 | 🔍 | ⏳ PII |
| 2 | `/pos/v1/GetMemberOwnCoupon` | 查詢會員優惠券 | 🔍 | ⏳ |
| 3 | `/pos/v1/GetMemberPoint` | 查詢會員紅利點數 | 🔍 | ⏳ |
| 4 | `/pos/v1/GetPOSOrderList` | 取得線下交易紀錄清單 | 🔍 | ⏳ |
| 5 | `/pos/v1/GetPOSOrderSummary` | 取得線下交易紀錄資訊 | 🔍 | ⏳ |
| 6 | `/pos/v1/QueryPOSActions` | 取得 POS 機操作紀錄 | 🔍 | ⏳ |
| 7 | `/pos/v1/CreateOrderPOSAction` | 建立訂單 POS 操作紀錄 | ✏️ | ⛔ |
| 8 | `/pos/v1/CreatePOSOrder` | 建立線下交易 | ✏️ | ⛔ |
| 9 | `/pos/v1/RedeemCoupons` | 核銷優惠券 POS 操作 | ✏️ | ⛔ |
| 10 | `/pos/v1/ReturnCoupons` | 歸還優惠券 POS 操作 | ✏️ | ⛔ |
| 11 | `/pos/v1/ReturnOrderPOSAction` | 取消單退還點券 POS 操作 | ✏️ | ⛔ |
| 12 | `/pos/v1/SetOuterMemberId` | 綁定品牌會員編號 | ✏️ | ⛔ |

---

## Cat.9 Invoice 發票（13 端點）

Auth: `x-api-key` ｜ Method: POST ｜ 13 Query + 0 Write（全部唯讀）

| # | Path | 名稱 | Tag | 類型 | 狀態 |
|---|------|------|-----|------|------|
| 1 | `/ec/V2/NotIssueInvoiceSalesOrder/Get` | 訂單載具資料明細查詢 | 訂單載具 | 🔍 | ⏳ ※同 Cat.1 |
| 2 | `/ec/V2/NotIssueInvoiceSalesOrder/GetList` | 訂單載具資料清單查詢 | 訂單載具 | 🔍 | ⏳ ※同 Cat.1 |
| 3 | `/ec/V2/SalesOrder/GetFinalList` | 主單載具資料清單查詢 | 訂單載具 | 🔍 | ⏳ |
| 4 | `/ec/V2/NotIssueInvoiceSalesOrder/GetShippingFailFeeList` | 逾期未取運費載具資料查詢 | 開立運費發票 | 🔍 | ⏳ |
| 5 | `/ec/V2/RefundRequest/GetSalesOrderFeeRefund` | 運費退款單明細查詢 | 運費退款 | 🔍 | ⏳ |
| 6 | `/ec/V2/RefundRequest/GetSalesOrderFeeRefundList` | 運費退款單清單查詢 | 運費退款 | 🔍 | ⏳ |
| 7 | `/ec/V2/ReturnGoodsOrder/Get` | 退貨單查詢（發票） | 退貨資料 | 🔍 | ⏳ ※同 Cat.1 |
| 8 | `/ec/V2/ReturnGoodsOrder/GetList` | 退貨清單查詢（發票） | 退貨資料 | 🔍 | ⏳ ※同 Cat.1 |
| 9 | `/ec/V2/RechargeReceipt/Get` | 補收單明細查詢（發票） | 補收資料 | 🔍 | ⏳ ※同 Cat.1 |
| 10 | `/ec/V2/RechargeReceipt/GetList` | 補收單清單查詢（發票） | 補收資料 | 🔍 | ⏳ ※同 Cat.1 |
| 11 | `/ec/V2/RefundRequest/GetSalesOrderRefund` | 訂單退款單明細查詢(含運費) | 訂單退款 | 🔍 | ⏳ |
| 12 | `/ec/V2/RefundRequest/GetSalesOrderRefundList` | 訂單退款單清單查詢(含運費) | 訂單退款 | 🔍 | ⏳ |
| 13 | `/ec/V2/MyInvoiceSalesOrder/Get` | 馬來西亞訂單發票明細查詢 | 馬來西亞 | 🔍 | ⏳ |

**註**：#1,2,7,8,9,10 與 Cat.1 Order 為同一端點（不同 Swagger spec），實作時只需一份。

---

## Cat.10 IMS Brand IMS 品牌版（26 端點）

Auth: `n1-api-key` ｜ REST-style（GET/POST/PUT）｜ 11 Query + 15 Write

| # | Method | Path | 名稱 | Tag | 類型 | 狀態 |
|---|--------|------|------|-----|------|------|
| 1 | GET | `/orders/list` | 查詢訂單清單 | Orders | 🔍 | ⏳ |
| 2 | GET | `/orders/{channelType}/{orderCode}` | 查詢訂單 | Orders | 🔍 | ⏳ |
| 3 | GET | `/fulfillment/list` | 查詢履約單清單 | Fulfillment | 🔍 | ⏳ |
| 4 | GET | `/fulfillment/{fulfillmentBatchId}` | 查詢指定履約單 | Fulfillment | 🔍 | ⏳ |
| 5 | GET | `/return-orders/list` | 查詢退貨單清單 | ReturnOrders | 🔍 | ⏳ |
| 6 | GET | `/return-orders/{channelType}/{returnOrderCode}` | 查詢退貨單詳細 | ReturnOrders | 🔍 | ⏳ |
| 7 | GET | `/stock-keeping-units/available-qtys` | 查詢 SKU 可賣量清單 | SKU | 🔍 | ⏳ |
| 8 | GET | `/warehouse-stocks/{warehouseId}/list` | 查詢倉庫庫存資料 | WarehouseStocks | 🔍 | ⏳ |
| 9 | GET | `/warehouse-stocks/{warehouseId}/calculate-rule` | 取得倉庫存計算規則 | WarehouseStocks | 🔍 | ⏳ |
| 10 | GET | `/warehouse-stocks/{warehouseId}/reserved-qtys` | 查詢倉庫庫存保留量 | WarehouseStocks | 🔍 | ⏳ |
| 11 | GET | `/warehouses/list` | 查詢倉庫清單 | Warehouses | 🔍 | ⏳ |
| 12–26 | POST/PUT | *(15 個寫入端點)* | 履約出貨/退貨處理/庫存異動/標籤產生/策略更新等 | — | ✏️ | ⛔ |

---

## Cat.11 IMS Channel IMS 通路版（21 端點）

Auth: `n1-api-key` ｜ REST-style（GET/POST/PUT/DELETE）｜ 9 Query + 12 Write

| # | Method | Path | 名稱 | Tag | 類型 | 狀態 |
|---|--------|------|------|-----|------|------|
| 1 | GET | `/products` | 取得商品資料 | Products | 🔍 | ⏳ |
| 2 | GET | `/salepages/list` | 查詢賣場檔清單 | SalePages | 🔍 | ⏳ |
| 3 | GET | `/salepages/{salePageId}` | 取得賣場檔資料 | SalePages | 🔍 | ⏳ |
| 4 | GET | `/fulfillment/list` | 查詢履約單清單 | Fulfillment | 🔍 | ⏳ |
| 5 | GET | `/fulfillment/{fulfillmentBatchId}` | 查詢指定履約單 | Fulfillment | 🔍 | ⏳ |
| 6 | GET | `/reverse-fulfillment/list` | 查詢逆向履約單清單 | ReverseFulfillment | 🔍 | ⏳ |
| 7 | GET | `/reverse-fulfillment/{id}` | 查詢指定逆向履約單 | ReverseFulfillment | 🔍 | ⏳ |
| 8 | GET | `/proposals/list` | 查詢提報單清單 | Proposals | 🔍 | ⏳ |
| 9 | GET | `/proposals/{proposalId}` | 查詢指定提報單 | Proposals | 🔍 | ⏳ |
| 10–21 | POST/PUT/DELETE | *(12 個寫入端點)* | 建立商品/賣場/提報/出貨/退貨/圖片管理等 | — | ✏️ | ⛔ |

---

## Cat.12 Payments 金流（30 端點）

Auth: `N1-API-KEY` + `N1-DATA-SIGNATURE`（HMAC-SHA256）｜ REST-style ｜ 11 Query + 18 Write + 1 Callback

| # | Method | Path | 名稱 | Tag | 類型 | 狀態 |
|---|--------|------|------|-----|------|------|
| 1 | GET | `/v2/trades/{tradeId}` | 交易查詢 | Payments | 🔍 | ⏳ |
| 2 | GET | `/v2/trades/{tradeId}/record` | 交易歷程查詢 | Payments | 🔍 | ⏳ |
| 3 | GET | `/v2/stored-value/accounts/{id}` | 儲值帳號查詢 | StoredValue | 🔍 | ⏳ |
| 4 | GET | `/v2/stored-value/accounts/{id}/detail` | 儲值帳號詳細資訊 | StoredValue | 🔍 | ⏳ |
| 5 | GET | `/v2/stored-value/accounts/{id}/transactions` | 儲值帳號交易紀錄 | StoredValue | 🔍 | ⏳ |
| 6 | GET | `/v2/stored-value/withdrawals` | 儲值金提領查詢 | StoredValue | 🔍 | ⏳ |
| 7 | GET | `/v2/stored-value/accounts/{id}/withdrawals/{code}/records` | 儲值金提領歷程 | StoredValue | 🔍 | ⏳ |
| 8 | POST | `/v2/promotion-bin-code/verify-bin-code` | BIN 碼驗證 | Promotions | 🔍 | ⏳ |
| 9 | GET | `/v2/ledgers/requests/{transferCode}` | 帳務交易查詢 | Ledgers | 🔍 | ⏳ |
| 10 | GET | `/v2/payments/payment-methods` | 查詢綁定支付方式（商店會員） | Binding | 🔍 | ⏳ |
| 11 | GET | `/v2/payments/payment-methods/{bindingToken}` | 查詢綁定支付方式（Token） | Binding | 🔍 | ⏳ |
| 12–29 | POST/DELETE | *(18 個寫入端點)* | 交易請求/請款/退款/儲值/提領/收款連結/BIN碼/帳務等 | — | ✏️ | ⛔ |
| 30 | POST | `/{callback-path}` | 交易結果通知 | — | 📨 | — Webhook |

---

## Cat.13 Payments Stored Value 儲值中心 POS（10 端點）

Auth: `N1-API-KEY` + `N1-DATA-SIGNATURE` ｜ preview 版本 ｜ 4 Query + 5 Write + 1 Callback

| # | Method | Path | 名稱 | 類型 | 狀態 |
|---|--------|------|------|------|------|
| 1 | GET | `/v2/stored-value/accounts/{id}` | 儲值帳號查詢 | 🔍 | ⏳ ※同 Cat.12 |
| 2 | GET | `/v2/stored-value/accounts/{id}/detail` | 儲值帳號詳細 | 🔍 | ⏳ ※同 Cat.12 |
| 3 | GET | `/v2/stored-value/accounts/{id}/transactions` | 交易紀錄 | 🔍 | ⏳ ※同 Cat.12 |
| 4 | GET | `/v2/stored-value/withdrawals` | 儲值金提領查詢 | 🔍 | ⏳ ※同 Cat.12 |
| 5–9 | POST | *(5 個寫入端點)* | 提領申請/更新/儲值金扣除/退款/取消 | ✏️ | ⛔ |
| 10 | POST | `/{callback-path}` | 交易結果通知 | 📨 | — Webhook |

**註**：#1-4 與 Cat.12 Payments StoredValue tag 完全重疊。

---

## Cat.14 Member 會員 Connect Cloud（21 端點）

Auth: `ny-api-token` / `n1-api-key` ｜ REST-style（GET/POST/PATCH/PUT/DELETE）｜ 8 Query + 13 Write

| # | Method | Path | 名稱 | Tag | 類型 | 狀態 |
|---|--------|------|------|-----|------|------|
| 1 | GET | `/v1/members/api/members` | 會員查詢 | Member | 🔍 | ⏳ PII |
| 2 | GET | `/v1/members/api/query-members` | 會員篩選 | Member | 🔍 | ⏳ PII |
| 3 | GET | `/v1/tags/api/batch-get-tag-keys` | 查詢標籤群組內標籤 | Member-Tag | 🔍 | ⏳ |
| 4 | GET | `/v1/tags/api/get-tag-key` | 標籤查詢 | Member-Tag | 🔍 | ⏳ |
| 5 | GET | `/v2/member-collections/query` | 取得客群清單(offset) | Member-Collection | 🔍 | ⏳ |
| 6 | GET | `/v2/member-collections/query-by-cursor` | 取得客群清單(cursor) | Member-Collection | 🔍 | ⏳ |
| 7 | GET | `/v2/member-collections/{collectionId}` | 取得客群資料 | Member-Collection | 🔍 | ⏳ |
| 8 | GET | `/v2/member-collections/{id}/histories` | 取得客群異動歷程 | Member-Collection | 🔍 | ⏳ |
| 9–21 | POST/PATCH/PUT/DELETE | *(13 個寫入端點)* | 加入會員/貼標籤/移除標籤/批次操作/新增客群/更新客群等 | — | ✏️ | ⛔ |

---

## Cat.15 SalePage Search 商品頁搜尋（1 端點）

Auth: `n1-api-key` ｜ v0.0.0（實驗版）

| # | Method | Path | 名稱 | 類型 | 狀態 |
|---|--------|------|------|------|------|
| 1 | POST | `/api/salepages:create-data-sync` | 建立資料同步請求 | ✏️ | ⛔ |

---

## Cat.16 DataSync Webhook（1 端點）

Auth: 商家實作回呼

| # | Method | Path | 名稱 | 類型 | 狀態 |
|---|--------|------|------|------|------|
| 1 | POST | `/DataSync/UploadCompleted` | 通知檔案上傳完成 | 📨 | — Webhook |

---

## 已納入工具（17 個）

### 訂單 — Order（5 個）

| # | Tool 名稱 | API Endpoint | 說明 |
|---|-----------|-------------|------|
| 1 | `get_order_list` | `POST /ec/V2/SalesOrder/GetList` | 訂單清單查詢（日期範圍≤7天、狀態、配送方式篩選） |
| 2 | `get_order_detail` | `POST /ec/V2/SalesOrder/Get` | 訂單明細查詢（TGCode 或 TMCode 查詢） |
| 3 | `get_return_order_list` | `POST /ec/V2/ReturnGoodsOrder/GetList` | 退貨單清單查詢（日期範圍≤7天、退貨狀態篩選） |
| 4 | `get_return_order_detail` | `POST /ec/V2/ReturnGoodsOrder/Get` | 退貨單明細查詢（ReturnGoodDetailId 查詢） |
| 5 | `get_exchange_order_list` | `POST /ec/V2/ChangeGoodsOrder/GetList` | 換貨單清單查詢（日期範圍≤7天、換貨狀態篩選） |

### 商品 — Product / Salepage（7 個）

| # | Tool 名稱 | API Endpoint | 說明 |
|---|-----------|-------------|------|
| 6 | `get_product_list` | `POST /ec/V1/SalePage/GetSKUList` | 商品 SKU 清單查詢（日期、上下架、分類篩選）※V1 legacy |
| 7 | `get_product_detail` | `POST /ec/V1/SalePage/GetMainDetail` | 商品完整明細查詢（SalePageId）※V1 legacy |
| 8 | `get_product_stock` | `POST /ec/V1/SalePage/GetStock` | 商品庫存查詢（SalePageId，可指定 SKU） |
| 9 | `get_shop_categories` | `POST /ec/V1/Category/GetShopCategory` | 商店自訂分類清單查詢 |
| 10 | `get_category_tree` | `POST /ec/V1/Category/GetCategory` | 91app 系統商品分類樹狀查詢 |
| 11 | `get_shop_payment_methods` | `POST /ec/V1/Shop/GetPayment` | 商店付款方式清單查詢 ※V1 legacy |
| 12 | `get_shop_shipping_methods` | `POST /ec/V1/Shop/GetShipping` | 商店配送方式清單查詢 |

### 促銷 — Promotion（3 個）

| # | Tool 名稱 | API Endpoint | 說明 |
|---|-----------|-------------|------|
| 13 | `get_promotions` | `POST /ec/V2/Promotion/GetPromotions` | 折扣活動清單查詢（時間、狀態、類型篩選，最多 1000 筆） |
| 14 | `get_promotion_detail` | `POST /ec/V2/Promotion/GetPromotionDetail` | 折扣活動完整明細查詢（活動 ID） |
| 15 | `get_promotion_salepages` | `POST /ec/V2/Promotion/GetPromotionSalePages` | 折扣活動適用商品清單查詢 |

### 物流 — Delivery（2 個）

| # | Tool 名稱 | API Endpoint | 說明 |
|---|-----------|-------------|------|
| 16 | `get_shipping_order` | `POST /ec/V2/ShippingOrder/Get` | 貨運單查詢（配送狀態、物流商、收件資訊；含 PII） |
| 17 | `get_shipping_countries` | `POST /ec/V2/Shop/GetShippingCountryList` | 配送國家清單查詢 |

---

## 統計按分類

| 領域 | 已實作 ✅ | 查詢暫緩 ⏳ | 寫入排除 ⛔ | Webhook 📨 | 合計 |
|------|---------|-----------|-----------|-----------|------|
| Cat.1 訂單 | 5 | 8 | 3 | 0 | 16 |
| Cat.2 物流 | 2 | 10 | 22 | 0 | 34 |
| Cat.3 商品頁 | 4(+3 legacy) | 8 | 12 | 0 | 24 |
| Cat.4 促銷 | 3 | 6 | 11 | 0 | 20 |
| Cat.5 門市 | 0 | 2 | 3 | 0 | 5 |
| Cat.6 會員等級 | 0 | 0 | 1 | 0 | 1 |
| Cat.7 多語系 | 0 | 1 | 1 | 0 | 2 |
| Cat.8 POS | 0 | 6 | 6 | 0 | 12 |
| Cat.9 發票 | 0 | 13 | 0 | 0 | 13 |
| Cat.10 IMS 品牌 | 0 | 11 | 15 | 0 | 26 |
| Cat.11 IMS 通路 | 0 | 9 | 12 | 0 | 21 |
| Cat.12 金流 | 0 | 11 | 18 | 1 | 30 |
| Cat.13 儲值 POS | 0 | 4 | 5 | 1 | 10 |
| Cat.14 會員 CC | 0 | 8 | 13 | 0 | 21 |
| Cat.15 商品搜尋 | 0 | 0 | 1 | 0 | 1 |
| Cat.16 DataSync | 0 | 0 | 0 | 1 | 1 |
| **合計** | **17** | **97** | **123** | **3** | **237** |

**去除跨分類重複**（Cat.9 與 Cat.1、Cat.13 與 Cat.12）後，不重複端點約 **221 個**。

---

## 架構備註

1. **HTTP 方法**：Categories 1-9（Admin API 核心）所有端點均使用 `POST` + JSON body，包含查詢操作。Categories 10-14 使用標準 REST（GET/POST/PUT/DELETE/PATCH）。
2. **認證方式**：
   - `x-api-key`：Admin API 核心（Cat.1-9），從 91APP OMNI 管理後台取得
   - `n1-api-key`：IMS 系列（Cat.10-11）+ 商品搜尋（Cat.15）
   - `N1-API-KEY` + `N1-DATA-SIGNATURE`（HMAC-SHA256）：金流（Cat.12-13）
   - `ny-api-token` / `n1-api-key`：會員 Connect Cloud（Cat.14）
3. **ShopId**：大多數 Admin API（Cat.1-9）必填。透過 `APP_91APP_SHOP_ID` 環境變數設定預設值。
4. **PII 注意**：`get_shipping_order`、`get_order_detail` 回傳含收件人姓名、電話、地址等個人資料。POS 會員 API 含會員基本資料、紅利點數。使用時請遵守隱私規範。
5. **分頁**：Admin API 使用 `Position`（0-based offset）+ `Count`，非 cursor-based。Member Connect Cloud 支援 offset 與 cursor 兩種分頁。
6. **V1 Legacy 端點**：`GetSKUList`、`GetMainDetail`、`GetPayment` 等 V1 端點未列入 Swagger 但確認可用，已納入工具實作。
