# Estimate — SWP và giờ

**Báo cáo HTML của skill chấm SWP:** [reports/swp-report.html](reports/swp-report.html) (xem trực tiếp: https://htmlpreview.github.io/?https://github.com/haiht-1795/lab5-product-b-backlog/blob/main/reports/swp-report.html)

Skill: [skills/swp-scoring](skills/swp-scoring/SKILL.md), tự viết (máy không có skill chấm SWP chính thức). Quy trình gồm 4 bước:
1. AI chấm Scope/Complexity cho từng issue khi break, ghi vào `backlog/backlog.json`.
2. Skill tính SWP, flag lỗi độ hạt và chọn issue mẫu.
3. Người review đọc spec LAB-4 của từng mẫu rồi ghi quyết định vào [backlog/swp-review.json](backlog/swp-review.json).
4. Chạy lại skill, ghi SWP đã chốt lên trường `SWP` của Project.

**Thang chấm:** Scope 1–5 (1 trường → luồng xuyên module) × Complexity 1–5 (CRUD → tích lũy nhiều ngày/offline mã hóa). **+1 Complexity** cho quy tắc lấy ngưỡng từ luật chưa xác minh (cờ `legal`, ở dự án này là giờ lái 2024). SWP = Fib(S × C): ≤2→1 · 3–4→2 · 5–6→3 · 8–10→5 · 12→8 · 15–16→13 · ≥20→21 (21 = phải tách).

## 1. Issue mẫu skill chọn để kiểm

Skill chọn 26/80 issue theo 4 luật: R1 có flag độ hạt, R2 issue pháp lý SWP ≥ 8, R3 chấm lệch |S − C| ≥ 2, R4 issue lớn nhất mỗi epic chưa được chọn (đối chứng).
Lần chạy đầu có 13 issue bị flag (12 `SUB-BIG`, 1 `NEED-SUB`). Lỗi nằm ở cách chia sub-issue, không ở SWP, nên đã chia lại sub-issue và giữ nguyên điểm. Lần chạy thứ hai không còn flag.
Người review **sửa 2 issue**, giữ nguyên 24 issue (lý do giữ ghi ở từng dòng):

| Issue | Lý do skill chọn | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|---|
| #27 Chế độ thiết bị dùng chung, trang chủ hàng đợi theo vai trò, thời hạn lưu/legal hold | R3 chấm lệch |S−C| ≥ 2 | S4 × C2 → 5 | Giữ 5 | Giữ 5. Gộp 3 tính năng nhỏ chưa có spec (FT-01-05/08/09) làm chỗ giữ effort; sẽ tách 3 issue khi spec được duyệt. Không xếp sprint. |
| #28 Master SKU, vị trí, NCC, thiết bị + sửa seed theo RFP R-01/R-02 | R3 chấm lệch |S−C| ≥ 2 | S4 × C2 → 5 | Giữ 5 | Giữ 5. 4 master CRUD đơn giản (C2) nhưng phải sửa seed theo R-01/R-02 (G-01/02/07/23/32): S4 đúng. |
| #31 PolicyResolver.effectiveAt(t) + exclusion constraint không chồng lấn hiệu lực | R3 chấm lệch |S−C| ≥ 2 | S2 × C4 → 5 | Giữ 5 | Giữ 5. Scope nhỏ nhưng exclusion constraint tstzrange + quy tắc không hồi tố khó test: C4 đúng. |
| #43 SCR-022 xác nhận nhập: tạo lô bất biến idempotent, đặt đúng vị trí, in nhãn GS1-128 | R1 flag: SUB-BIG | S3 × C4 → 8 | Giữ 8 | Giữ 8. STUB OQ-15 (trùng số lô) nên k=1.25 là hợp lý. Đã tách 3 sub-issue theo flag SUB-BIG. |
| #48 Máy trạng thái lô + sổ tồn stock_balance/inventory_movement | R1 flag: SUB-BIG | S4 × C4 → 13 | Giữ 13 | Giữ 13. Sổ tồn là nền cho F05/F06; đã tách 4 sub-issue ≤ 13h theo flag SUB-BIG. |
| #58 Port @ycl/rules expiry + deliveryWindow + dateReversal từ prototype, sửa G-03/04/06/25 | R1 flag: SUB-BIG | S4 × C4 → 13 | Giữ 13 | Giữ 13. Port từ prototype nhưng phải sửa 4 lỗi G-03/04/06/25; đã tách 4 sub-issue theo flag. |
| #64 Phân bổ nguyên tử 1 transaction/lần chạy, khóa dòng theo thứ tự | R1 flag: SUB-BIG | S3 × C4 → 8 | Giữ 8 | Giữ 8. Đã chia lại sub-issue 50/50 (test đồng thời tốn ngang phần code). |
| #70 SCR-051 quét PICK/LOAD, kiểm lại G2/G3 theo lô thực quét | R1 flag: SUB-BIG | S4 × C4 → 13 | Giữ 13 | Giữ 13. Màn quét 2 chế độ + kiểm lại G2/G3; đã chỉnh tỉ lệ sub-issue để mỗi sub ≤ 16h. |
| #76 Xác nhận xuất G4: đọc mốc trong transaction, khóa theo (customer_id, sku_id) | R1 flag: SUB-BIG | S3 × C4 → 8 | Giữ 8 | Giữ 8. Đã chia sub 50/50. |
| #79 Dỡ đơn bị chặn ở G4, tạo phiên bản tuyến mới để kiểm giờ lại | R1 flag: SUB-BIG | S3 × C4 → 8 | **S4 × C4 → 13** | Tăng S 3 → 4 (SWP 8 → 13). Skill chấm như việc nội bộ F06, nhưng dỡ đơn kéo theo tạo version tuyến mới và chạy lại kiểm giờ lái 2024 (xuyên outbound + routing-duty). Đã tách 5 sub-issue. |
| #87 Dựng tuyến theo ngày: gán đơn vào xe theo ngăn vùng nhiệt, danh sách chưa gán có lý do | R1 flag: SUB-BIG | S4 × C4 → 13 | Giữ 13 | Giữ 13. Đã chỉnh tỉ lệ sub-issue. |
| #102 SCR-017 bộ quy tắc giờ ràng buộc có version: 8 tham số DUTY-*, cờ verified_by_legal | R2 ràng buộc pháp lý, SWP ≥ 8 | S3 × C4 (+1 pháp lý) → 8 | Giữ 8 | Giữ 8. +1 pháp lý đúng: 8 tham số DUTY-* và cờ verified_by_legal là chỗ duy nhất giữ giá trị luật. |
| #106 Mô hình timeline tài xế: ngày = 24h từ đầu ca, gộp giờ thực tế + tuyến đã công bố khác | R2 ràng buộc pháp lý, SWP ≥ 8 | S3 × C5 (+1 pháp lý) → 13 | Giữ 13 | Giữ 13. Chia ngày theo đầu ca + tuyến qua đêm + gộp nhiều tuyến là phần rủi ro nhất của validator (OQ-29). |
| #111 Kiểm DUTY-BIND-D/M/Y (13–15h, 284h, 3.300h) và DUTY-REST (11h/9h) | R2 ràng buộc pháp lý, SWP ≥ 8 | S3 × C4 (+1 pháp lý) → 8 | Giữ 8 | Giữ 8. Tích lũy tháng/năm dựa trên timeline của #106 nên không tăng thêm. |
| #114 Kiểm DUTY-DRV-2D (tham số BOTH/EITHER) và DUTY-DRV-2W (khối 2 tuần từ 起算日) | R3 chấm lệch |S−C| ≥ 2 | S2 × C5 (+1 pháp lý) → 5 | Giữ 5 | Giữ 5. Đã cân nhắc tăng S do thêm mode BOTH/EITHER, nhưng chỉ là nhánh trong cùng hàm; ca thiếu dữ liệu D+1 được test ở #133. |
| #115 DUTY-CONT ≤ 4h + tự chèn điểm nghỉ (30 phút, mỗi lần ≥ 10 phút) | R2 ràng buộc pháp lý, SWP ≥ 8 | S3 × C4 (+1 pháp lý) → 8 | Giữ 8 | Giữ 8. |
| #121 API duty-checks + lưu kết quả 8 mã + panel/timeline đỏ trên SCR-060 | R1 flag: SUB-BIG | S4 × C3 → 8 | Giữ 8 | Giữ 8. Hiển thị không chịu +1 pháp lý (legal=false) là đúng. Đã tách 3 sub-issue theo flag. |
| #125 Cổng công bố: kiểm lại trong transaction, gắn version quy tắc, xác nhận WARN, không override, không hồi tố | R2 ràng buộc pháp lý, SWP ≥ 8 | S3 × C5 (+1 pháp lý) → 13 | **S3 × C4 (+1 pháp lý) → 8** | Giảm C 4 → 3 (SWP 13 → 8). Cộng +1 pháp lý bị tính trùng: ngưỡng luật nằm ở #111…#118, cổng công bố chỉ gọi lại validator trong transaction và gắn version. Phần không hồi tố vẫn có sub-issue test riêng. |
| #133 Bộ test ranh giới giờ lái: 8 mã × (= giới hạn, + 1 phút) + kịch bản R-06 | R2 ràng buộc pháp lý, SWP ≥ 8 | S4 × C4 (+1 pháp lý) → 13 | Giữ 13 | Giữ 13. Bộ test biên là bằng chứng nghiệm thu ACC-SCH-01; không giảm. |
| #141 Lấy POD theo điều kiện giao 車上渡し / 軒先渡し | R1 flag: SUB-BIG | S3 × C4 → 8 | Giữ 8 | Giữ 8. OQ-38 BLOCK: không xếp sprint đến khi có trả lời. Đã tách 3 sub-issue. |
| #145 Hàng đợi offline IndexedDB mã hóa AES-GCM ≤ 8h, đồng bộ an toàn | R1 flag: SUB-BIG | S4 × C4 → 13 | Giữ 13 | Giữ 13 (65h). Rủi ro kỹ thuật cao nhất của F07; cần spike thiết kế trước. Đã tách 5 sub-issue. |
| #160 Alarm → hồ sơ sai lệch + cách ly lô liên quan trong cùng transaction | R1 flag: SUB-BIG | S3 × C4 → 8 | Giữ 8 | Giữ 8. Đã chia sub 50/50. |
| #167 Hồ sơ thu hồi, đối chiếu số lượng, thông báo thu hồi có duyệt | R4 SWP lớn nhất của epic (đối chứng) | S4 × C3 → 8 | Giữ 8 | Giữ 8 (đối chứng epic F10). Ước lượng thô vì F10 chỉ có ở mức dữ liệu. |
| #173 6 báo cáo xuất/giao/nhiệt | R3 chấm lệch |S−C| ≥ 2 | S4 × C2 → 5 | Giữ 5 | Giữ 5. 6 báo cáo dùng khung của #170, độ khó thấp. |
| #176 ERP → đơn qua SFTP: checksum, khóa, từ chối cả file | R4 SWP lớn nhất của epic (đối chứng) | S3 × C3 → 5 | Giữ 5 | Giữ 5 (đối chứng epic F12). |
| #183 Đối chiếu + business review, gồm lịch sử giao làm mốc đảo ngày | R1 flag: NEED-SUB | S3 × C3 → 5 | Giữ 5 | Giữ 5. Đã thêm 2 sub-issue theo flag NEED-SUB; phần lịch sử giao chờ OQ-43. |

Hai lần sửa bù trừ nhau (+5 / −5) nên tổng SWP không đổi (482). Đó là trùng hợp, không phải để cân tổng: một lần sửa vì skill bỏ sót phạm vi xuyên module do ràng buộc giờ lái, một lần vì skill cộng trùng +1 pháp lý.

## 2. Cách quy ra giờ

- **Cách đã chọn:** quy ước đổi SWP ra giờ, không ước giờ trực tiếp từng issue.
- **Vì sao:** (1) tái lập được: cùng S, C cho cùng giờ, ai chạy cũng ra một kết quả; (2) người review chỉ tranh luận một con số (SWP), giờ tự theo; (3) ước giờ trực tiếp 80 issue bằng AI cho kết quả không ổn định giữa các lần chạy, và không có dữ liệu thực tế của đội để hiệu chỉnh.
- **Quy tắc:** `Giờ = SWP × 4h × k`, làm tròn đến giờ.
  - 4h = giờ **tập trung** cho 1 SWP, gồm code + unit test + sửa sau review (PREMISE A-02). Ví dụ SWP 5 (một use case qua API + UI) = 20h ≈ 3,3 ngày tập trung.
  - `k = 1.25` khi issue làm theo đề xuất tạm của OQ ở chế độ STUB/BLOCK (phần dễ phải làm lại khi khách trả lời). CFG không cộng, vì chỉ đọc tham số.
  - Sub-issue: giờ issue cha × tỉ lệ khai báo; sub cuối nhận phần dư để tổng khớp. Sub-issue không có SWP riêng.
- **Áp dụng nhất quán:** công thức nằm trong code của skill ([swp-score.py](skills/swp-scoring/scripts/swp-score.py)), không ai gõ tay giờ lên Project; script [github-project-sync.py](scripts/github-project-sync.py) chỉ đọc kết quả của skill. Đổi quy ước thì chạy lại skill và sync, mọi issue đổi theo.
- **Năng lực sprint:** 6 giờ tập trung/người/ngày (PREMISE A-01), dùng chung cho kế hoạch sprint và cho so sánh với LAB-1.

## 3. Tổng theo epic

| Epic | Số issue | Số sub-issue | Tổng SWP | Tổng giờ | Ghi chú |
|---|---:|---:|---:|---:|---|
| #1 Nền tảng kỹ thuật, xác thực, phân quyền, audit | 9 | 4 | 44 | 176 | 1 chờ spec/thiết kế |
| #2 Master & chính sách nhiệt có phiên bản | 7 | 0 | 28 | 112 | — |
| #3 Nhập hàng & kiểm nhập | 6 | 7 | 35 | 150 | 2 STUB/BLOCK (k=1.25); 1 chờ spec/thiết kế |
| #4 Tồn kho, lô, cách ly | 6 | 4 | 31 | 126 | 1 STUB/BLOCK (k=1.25); 2 chờ spec/thiết kế |
| #5 Đơn hàng & phân bổ (消費/賞味, 1/3·1/2, cấm đảo ngày, FEFO) | 6 | 6 | 39 | 159 | 1 STUB/BLOCK (k=1.25); 1 chờ spec/thiết kế |
| #6 Pick, load, kiểm trước xuất, xác nhận xuất (4 chốt) | 6 | 11 | 44 | 189 | 1 STUB/BLOCK (k=1.25); 1 chờ spec/thiết kế |
| #7 Lập tuyến & bản đồ (phần không phụ thuộc luật giờ lái) | 5 | 10 | 38 | 157 | 1 STUB/BLOCK (k=1.25) |
| #8 ⚠ Giới hạn giờ lái xe tải 2024 (改善基準告示) | 13 | 23 | 90 | 371 | 8 issue +1 pháp lý; 3 STUB/BLOCK (k=1.25) |
| #9 Giao hàng, POD offline, khiếu nại | 4 | 12 | 34 | 162 | 3 STUB/BLOCK (k=1.25); 4 chờ spec/thiết kế |
| #10 Giám sát nhiệt, sai lệch, HACCP | 6 | 6 | 34 | 141 | 1 STUB/BLOCK (k=1.25); 1 chờ spec/thiết kế |
| #11 Truy xuất & thu hồi | 2 | 2 | 13 | 52 | 2 chờ spec/thiết kế |
| #12 Báo cáo, KPI, xuất kiểm toán | 4 | 2 | 23 | 92 | 3 chờ spec/thiết kế |
| #13 Tích hợp ngoài (ERP SFTP, archive, giám sát interface) | 3 | 0 | 11 | 44 | — |
| #14 Chuyển đổi dữ liệu | 3 | 4 | 18 | 77 | 1 STUB/BLOCK (k=1.25); 1 chờ spec/thiết kế |
| **Tổng** | **80** | **91** | **482** | **2008** | |

## 4. So với estimate LAB-1

LAB-1 ước man-day (8h) cho phần **build FE + BE + UT** của 74 tính năng, cộng 25 MD dựng platform, tổng 610 MD. Các pha thiết kế, IT, ST, UAT, migration, đào tạo, PM được tính theo tỉ lệ và hạng mục cố định ngoài con số này. Vì vậy chỉ so phần build. Giờ LAB-5 quy ra MD theo **6 giờ tập trung/ngày** (cùng cơ sở với năng lực sprint), không chia 8. Tính năng LAB-1 xuất hiện ở nhiều epic (FT-08-04) được chia đều.

| Phần (epic) | LAB-1 (MD) | LAB-5 (giờ → MD @6h) | Chênh | Vì sao |
|---|---:|---:|---:|---|
| E01 Nền tảng kỹ thuật, xác thực, phân quyền, audit | 82.0 | 176 → 29.3 | -64% | LAB-1 có 25 MD dựng platform + 3 tính năng chưa có spec (FT-01-05/08/09) nay chỉ là 1 issue thô; một phần IaC/CI LAB-1 tính ở hạng mục cố định. |
| E02 Master & chính sách nhiệt có phiên bản | 43.0 | 112 → 18.7 | -57% | Chưa issue hóa các màn master mức List; FT-02-07 (version giờ lái) chuyển sang E08. |
| E03 Nhập hàng & kiểm nhập | 48.0 | 150 → 25.0 | -48% | SCR-020 hẹn nhập và SCR-023 vùng nhiệt tạm (FT-03-01/06, 11 MD) mới có issue thiết kế, phần làm chưa ước lượng (OQ-63 BLOCK). |
| E04 Tồn kho, lô, cách ly | 40.0 | 126 → 21.0 | -48% | Kiểm kê mù FT-04-04 (12 MD) mới có issue thiết kế (OQ-62 BLOCK). |
| E05 Đơn hàng & phân bổ (消費/賞味, 1/3·1/2, cấm đảo ngày, FEFO) | 55.0 | 159 → 26.5 | -52% | Tái dùng expiry-rules và allocation-engine đã có unit test ở prototype LAB-2 (PREMISE LAB-4: chỉ giữ module quy tắc thuần); SCR-040/041 còn mức List. |
| E06 Pick, load, kiểm trước xuất, xác nhận xuất (4 chốt) | 32.0 | 189 → 31.5 | -2% | Gần khớp: #79 (dỡ đơn → version tuyến mới → kiểm giờ lái lại, task-breakdown §3) tăng effort, bù phần giảm do tái dùng. |
| E07 Lập tuyến & bản đồ (phần không phụ thuộc luật giờ lái) | 24.0 | 157 → 26.2 | +9% | Gần khớp: thêm adapter bản đồ + fake provider (PREMISE S-06), bản đồ chuyển từ F12 sang đây. |
| E08 ⚠ Giới hạn giờ lái xe tải 2024 (改善基準告示) | 43.0 | 371 → 61.8 | +44% | Ràng buộc 2024 làm tăng effort: validator tách 5 issue theo nhóm mã, +1 Complexity pháp lý, bộ test biên #133 (PREMISE S-04), SCR-063 (S-01), SCR-062 (S-03), cổng công bố trong transaction. LAB-1 chưa có các phần này. |
| E09 Giao hàng, POD offline, khiếu nại | 53.0 | 162 → 27.0 | -49% | F07 chỉ có ở mức kiến trúc (ADR-009) → issue thô; OQ-38 BLOCK, OQ-39 STUB. |
| E10 Giám sát nhiệt, sai lệch, HACCP | 55.0 | 141 → 23.5 | -57% | HACCP FT-09-05…07 (19 MD) mới có issue thiết kế. |
| E11 Truy xuất & thu hồi | 32.0 | 52 → 8.7 | -73% | F10 chỉ ở mức dữ liệu → ước lượng thô, nhiều khả năng thiếu. |
| E12 Báo cáo, KPI, xuất kiểm toán | 50.0 | 92 → 15.3 | -69% | 12 báo cáo gộp 2 issue giữ chỗ: thấp hơn thực tế, phải estimate lại khi có spec. |
| E13 Tích hợp ngoài (ERP SFTP, archive, giám sát interface) | 22.0 | 44 → 7.3 | -67% | Bản đồ chuyển sang E07; schema ERP (OQ-41) chưa có. |
| E14 Chuyển đổi dữ liệu | 31.0 | 77 → 12.8 | -59% | Chưa có spec dữ liệu nguồn; LAB-1 tính đủ tool + lineage chi tiết. |
| **Tổng build (FE+BE+UT)** | **610** | **335** | **-45%** | Xem giải thích dưới bảng |

**Đọc bảng:**
- **Epic có ràng buộc đặc thù (E08) tăng khoảng 44%.** Đây là phần được break kỹ nhất. Ràng buộc 2024 làm phát sinh việc LAB-1 chưa thấy: tách validator, test biên, 2 màn thiếu spec, cổng công bố trong transaction (PREMISE S-01…S-05).
- **E06, E07 gần khớp.** Hai epic này có spec chi tiết ở LAB-4 và không có tính năng chờ thiết kế.
- **Các epic khác thấp hơn 48–73%, không phải vì làm nhanh hơn.** Phần lớn chênh đến từ chỗ chưa issue hóa: màn mức List, F07/F10–F13 chỉ có issue thô `needs-design`, các tính năng mới có issue thiết kế. Một phần nhỏ đến từ tái dùng module quy tắc của prototype.
- **Kết luận:** tổng LAB-5 (≈ 335 MD) **chưa thay được** con số LAB-1 để báo giá hay đổi mốc. Khi spec các phần còn thiếu xong, estimate sẽ tăng lại. Rủi ro này được theo dõi ở progress-report.md (R-06).
