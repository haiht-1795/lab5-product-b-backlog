# PREMISE — Backlog LAB-5 khác bản LAB-4 ở đâu

Gốc: bộ thiết kế LAB-4 `lab 4-AIDD` (nộp 2026-11-14), gồm PREMISE LAB-4 P-01…P-24 và sổ câu hỏi OQ-01…OQ-65.
Các giả định P-xx và câu hỏi OQ-xx của LAB-4 **vẫn giữ nguyên**, file này không lặp lại. Dưới đây chỉ ghi những gì LAB-5 thêm, bỏ hoặc sửa khi break task.
Mã dòng `S-xx`, `A-xx`, `D-xx` được các file khác trỏ tới.

## 1. Spec thêm / bỏ / sửa so với LAB-4

| # | Spec (mã/file) | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| S-01 | SCR-063 Nhập giờ thực tế tài xế (FT-08-06) | Thêm | Trước: P-09 LAB-4 chỉ nêu tên màn "SCR-063", không có screen spec, wireframe hay API. Sau: issue thiết kế + làm, spec tối thiểu nằm trong issue (trường giờ bắt đầu/kết thúc ca, lái, nghỉ, người nhập DSP/DRV, chỉ cho ngày D−1 trở về trước) | Chỗ hở phát hiện khi break: DUTY-BIND-M/Y và DUTY-REST cần giờ thực tế D−1 (DSG-DUTY-03 "thiếu actual D−1 → WARN"). Không có màn nhập thì validator không có dữ liệu thật, chỉ có kế hoạch. | #130, #106, #111 |
| S-02 | business-rules.md DSG-DUTY-01 (DUTY-DRV-2D) | Sửa | Trước: chỉ có cách đọc **BOTH** (cả 2 cặp ngày > 9h mới vi phạm), ghi chú "điểm tranh chấp trong review". Sau: thêm tham số `drv2d_mode ∈ {BOTH, EITHER}` vào `duty_rule_param`, mặc định BOTH, gắn với version quy tắc | Góp ý review LAB-4: reviewer độc lập đọc là EITHER, OQ-28 chưa có trả lời. Nếu code cứng một cách đọc thì khi khách chọn cách kia phải sửa code validator và test. | #114, #102, #133 |
| S-03 | SCR-062 Ghi sự cố bất khả kháng (FR-SCH-05) | Sửa | Trước: chỉ có API contract FM1–FM9 trong F08 technical-spec, "SCR-062 chưa có spec". Sau: issue gồm phần thiết kế màn (form theo FM1–FM9, link từ SCR-060) và làm | FT-08-05 là P1, DRV/DSP cần màn để ghi; RFP tách báo cáo tuân thủ và báo cáo sự cố. Không có màn thì yêu cầu FR-SCH-05 không nghiệm thu được. | #131, #132 |
| S-04 | F08 technical-spec §Verification, ACC-SCH-01 | Thêm | Trước: chỉ có ví dụ đơn lẻ (lái liên tục 4h01 → BLOCK). Sau: ma trận test 8 mã DUTY-* × 2 biên (= giới hạn → PASS theo L4, + 1 phút → vi phạm) + kịch bản tuyến qua đêm, nhiều tuyến/ngày, thiếu actual, đổi version luật | Ràng buộc RFP "lỗi nghiêm trọng khi chấm thầu" (T-13). Ví dụ đơn lẻ không bắt được lỗi `<` / `≤`, cũng không bắt được lỗi chia ngày. | #133 |
| S-05 | business-rules.md DUTY-OT-Y (960h/năm) | Sửa | Trước: ngưỡng có, công thức "giờ làm thêm" để mở (OQ-58). Sau: công thức là strategy cắm được theo version quy tắc, mặc định = ràng buộc − nghỉ − 8h/ngày (đề xuất LAB-4), làm ở mức STUB | Chỗ hở khi break: không thể viết tiêu chí Done cho một công thức chưa có. Tách strategy để khi khách trả lời chỉ đổi tham số, không đổi code gọi. | #118 |
| S-06 | architecture.md §4 IF-MAP-01 | Thêm | Trước: "nhà cung cấp và license do Yuki chọn". Sau: interface adapter + fake provider (dữ liệu tổng hợp) cho dev/test; adapter thật làm khi có OQ-35 | Chỗ hở khi break: F08 (ETA, cấm công bố khi ước tính > 24h) không test được nếu chưa có nhà cung cấp. | #92, #95 |

Không có thay đổi lớn về màn hình nên không đặt bản sửa spec trong repo; nội dung tối thiểu của S-01, S-03 nằm trong mô tả issue.

## 2. Giả định bổ sung

| # | Giả định | Chỗ spec/RFP để ngỏ | Ảnh hưởng tới issue/estimate |
|---|---|---|---|
| A-01 | Đội giả định 7 người: TL (50% code), BE1–BE3, FE1, QA1, BrSE (bán thời gian, lo OQ). Năng lực **6 giờ tập trung/người/ngày**, sprint 2 tuần = 10 ngày | RFP và LAB-1 chỉ có tổng MM, không có cơ cấu đội theo sprint | Năng lực Sprint ≈ 6 × 10 × (0.5 + 5) + BrSE ≈ 350 giờ; trường "Phụ trách (giả định)" trên Project |
| A-02 | Giờ ước lượng là **giờ tập trung** gồm code + unit test + sửa sau review; không gồm họp, không gồm IT/ST/UAT (LAB-1 tính các pha đó theo tỉ lệ riêng) | Đề không quy định đơn vị giờ | Khi so với LAB-1 (man-day 8h) quy đổi theo 6h/ngày, xem estimate.md §5 |
| A-03 | Sprint 1 giả lập 2026-11-16 → 2026-11-27; trạng thái và nhật ký ngày là **giả lập**, không phải dữ liệu thật | Đề yêu cầu "ít nhất 1 sprint giả lập" | progress-report.md, trường Status/Iteration trên Project |
| A-04 | Dữ liệu dev/test (tài xế, tuyến, giờ thực tế, logger) là dữ liệu tổng hợp; không dùng dữ liệu thật của khách | RFP chưa giao fixtures (PREMISE LAB-4 §3) | #133, #92, #154 dùng fixture tự tạo |
| A-05 | Issue chưa có spec màn (gắn `needs-design`) chỉ là chỗ giữ effort, **không xếp vào sprint** cho tới khi spec được duyệt | LAB-4 chỉ thiết kế sâu 7 feature; F07, F10–F13 ở mức kiến trúc/dữ liệu | 17 issue needs-design/thiết kế; skill SWP flag `DESIGN-SPRINT` nếu xếp nhầm |
| A-06 | Issue có OQ ở chế độ BLOCK (trừ issue làm rõ/thiết kế) không xếp sprint | Cột "Dev" của OQ LAB-4 | #141, #183 chưa xếp sprint |
| A-07 | Chuyển tuyến PUBLISHED → IN_PROGRESS làm cùng transaction xác nhận xuất (F06); khóa revision/hủy khi IN_PROGRESS làm ở F08 | F08 SM-801 ghi "F06 sở hữu transition" nhưng không nói thứ tự triển khai giữa 2 module | Transition ở #76, khóa ở #100, test chung ở #79 |
| A-08 | Seed dữ liệu dev/test theo bảng SKU của RFP R-02 (CHI-001 = bò 消費期限 mã 10 số, AMB-001 = gạo), không theo seed prototype | LAB-4 prototype-vs-design G-32 chỉ ghi lệch, chưa nói seed đích | DoD của #28 |

## 3. Hướng đã chốt

| # | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| D-01 | Cách đọc DUTY-DRV-2D (trung bình lái 2 ngày) | BOTH (thiết kế LAB-4) / EITHER (reviewer độc lập) | Làm cả hai bằng tham số `drv2d_mode`, mặc định BOTH, version quy tắc mang cờ `verified_by_legal = false` cho tới khi OQ-28 có trả lời (S-02) | Không tự quyết cách hiểu luật (nguyên tắc LAB-4). Tham số rẻ hơn sửa code sau UAT. |
| D-02 | Đặt phần nào của F08 vào epic giờ lái 2024 | LAB-4 để F08 là một feature (FR-SCH-01…05) | Tách 2 epic: E07 lập tuyến/bản đồ (phần không phụ thuộc luật) và E08 giờ lái 2024 (version quy tắc, validator, chèn nghỉ, cổng công bố, giờ thực tế, sự cố, test biên). Revision tuyến chung ở E07; gắn version quy tắc khi công bố ở E08 | Yêu cầu đề: tách riêng hạng mục chịu ràng buộc đặc thù để ước lượng và theo dõi rủi ro riêng. |
| D-03 | Lô cách ly sau alarm: cách ly ngay (BR-HACCP-01) hay đo lại 15 phút rồi mới cách ly (FIG-010, OQ-56) | LAB-4 để mở, ghi mâu thuẫn | Làm theo BR-HACCP-01 (cách ly ngay, #160); luồng đo lại/保留 chưa thành issue | Quy tắc chữ (BR) mạnh hơn hình minh họa; cách ly ngay là phương án an toàn thực phẩm. Đổi sang đo lại chỉ thêm trạng thái, không phá dữ liệu. |
| D-04 | Quy ra giờ: ước trực tiếp từng issue hay quy ước từ SWP | — (LAB-4 không estimate; LAB-1 ước man-day theo tính năng) | Quy ước `giờ = SWP × 4h × k` (k = 1.25 khi OQ STUB/BLOCK) | Nhất quán, tái lập được, người review chỉ phải tranh luận một con số (SWP). Chi tiết ở estimate.md §3. |
| D-05 | Tài xế nhận "bản tuyến mới nhất" (US-484) nằm ở F08 hay F07 | LAB-4: US-484 thuộc F08, nhưng màn tài xế thuộc F07 (mức kiến trúc) | API phát hành version ở E08 (#125); màn PWA ở E09 (#138), gắn nhãn `constraint:touch-duty-2024` | Tránh epic giờ lái phụ thuộc thiết kế PWA chưa có; vẫn truy vết được ràng buộc. |
