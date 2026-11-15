# Task breakdown — Product B (Yuki Cold Logistics)

Nguồn duy nhất của backlog là [backlog/backlog.json](backlog/backlog.json). Script đẩy lên GitHub ([scripts/github-issues-sync.py](scripts/github-issues-sync.py), [scripts/github-project-sync.py](scripts/github-project-sync.py)) và render các bảng của file này ([scripts/render-doc-tables.py](scripts/render-doc-tables.py)). Vì vậy số issue trong tài liệu luôn khớp với Project.

## 1. Nguyên tắc chia task

**Độ hạt — chia tới đâu thì dừng**

| Cấp | Là gì | Dừng chia khi | Mang số liệu gì |
|---|---|---|---|
| Epic | 1 feature LAB-1 (F01…F13). Riêng F08 tách 2 epic, ràng buộc 2024 thành **E08** (PREMISE D-02) | — | Tổng SWP/giờ của các issue con |
| Issue | 1 kết quả kiểm chứng được: 1 quy tắc/nhóm mã quy tắc, 1 màn kèm API, 1 luồng transaction, hoặc 1 việc làm rõ/thiết kế. Bám 1 dòng truy vết T-xx hoặc 1 user story của LAB-4 | Viết được tiêu chí Done một câu, kiểm được bằng test hay demo; SWP ≤ 13 (SWP 21 → bắt buộc tách issue) | **SWP** (đã review) + **giờ** |
| Sub-issue | Phần việc của 1 người trong 1 issue (BE / FE / test) | ≤ 16 giờ | Giờ (chia từ giờ issue cha) |

**Khi nào tách sub-issue:** issue > 24 giờ (thường SWP ≥ 8, hoặc SWP 5 có OQ STUB), hoặc issue cần nhiều người (BE + FE + QA). Skill [skills/swp-scoring](skills/swp-scoring/SKILL.md) tự flag `NEED-SUB` (issue > 24h chưa tách) và `SUB-BIG` (sub-issue > 16h). Lần chạy đầu bắt được 13 issue vi phạm, đã sửa hết (estimate.md §1).

**Không để task mơ hồ:** issue thiếu spec màn được gắn `needs-design` và không xếp sprint (PREMISE A-05). Issue chịu câu hỏi chưa trả lời mang nhãn `oq:CFG/STUB/BLOCK` theo cột "Dev" của OQ LAB-4.

**Định nghĩa xong (chung cho mọi issue)**
1. Đạt tiêu chí riêng của issue (mục "Định nghĩa xong" trong issue, lấy từ cột "Kiểm chứng" của constraint-traceability LAB-4).
2. Code review xong; unit test xanh trên CI; với issue quy tắc thì có test ranh giới.
3. Chỗ có ⏳ OQ làm đúng chế độ CFG/STUB/BLOCK, không hard-code đề xuất của vendor.
4. Issue `constraint:duty-2024`: ngưỡng đọc từ version quy tắc (`duty_rule_param`), không hằng số trong code.
5. Trạng thái trên Project là Done và issue được đóng.

**Cách dùng epic → issue → sub-issue trên Project**
- Dùng tính năng sub-issue của GitHub: epic là issue cha của issue, issue là cha của sub-issue. Cột *Parent issue* và *Sub-issues progress* tự cập nhật.
- Trường riêng: `Epic` (single-select E01…E14, dùng để Group by vì trường hệ thống Parent issue không nhóm được), `Cấp` (Epic/Issue/Sub-issue), `SWP` (chỉ ghi ở Issue; ở Epic là tổng), `Giờ ước lượng`, `Phụ trách (giả định)`, `Ràng buộc đặc thù`, `Iteration`, `Status` (Todo / In Progress / In Review / Blocked / Done).
- Khi cộng SWP hoặc giờ trên Project, lọc `Cấp = Issue` để không cộng trùng epic và sub-issue.
- Nhãn: `type:*`, `constraint:duty-2024`, `constraint:touch-duty-2024`, `oq:*`, `needs-design`.

## 2. Spec → issue

{{TABLE:spec-to-issue}}

## 3. Hạng mục chịu ràng buộc đặc thù: giới hạn giờ lái xe tải từ 2024 (改善基準告示)

Toàn bộ nằm ở epic #{E08} (nhãn `constraint:duty-2024`, trường `Ràng buộc đặc thù = Giờ lái 2024`). Ba issue ở epic khác bị ràng buộc kéo theo, gắn `constraint:touch-duty-2024`.

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Ngưỡng luật là bản tóm tắt, phải xác minh với nguồn chính thức (OPS-LAW-01, T-14) | #{I-0801} SCR-017 version quy tắc + cờ `verified_by_legal`; #{I-0802} làm rõ pháp lý với khách | Là nơi duy nhất giữ giá trị luật. Có rủi ro chờ khách (BLOCK) khác hẳn việc dev, nên tách issue làm rõ để theo dõi riêng trên board. |
| Định nghĩa "1 ngày" = 24h từ đầu ca, gộp nhiều tuyến/ngày, giờ thực tế D−1 (DSG-DUTY-03, OQ-29) | #{I-0803} timeline tài xế | Mọi mã DUTY-* dùng chung mô hình này; sai ở đây thì sai cả 8 mã. Tách ra để làm và review trước. |
| DUTY-BIND-D/M/Y 13–15h / 284h / 3.300h, DUTY-REST 11h/9h | #{I-0804} | Cùng cơ chế tích lũy ngày/tháng/năm. Gộp lại với 2D/2W thì vượt 13 SWP (skill flag SPLIT). |
| DUTY-DRV-2D (BOTH/EITHER còn tranh chấp), DUTY-DRV-2W 44h × 2 tuần | #{I-0805} | Phụ thuộc OQ-28; tách để nếu khách đổi cách đọc chỉ đổi đúng issue này (PREMISE S-02, D-01). |
| DUTY-CONT ≤ 4h + tự chèn nghỉ 30 phút / ≥ 10 phút (FR-SCH-03) | #{I-0806} | Vừa là kiểm vừa sinh dữ liệu (BREAK auto_inserted); phụ thuộc OQ-31, OQ-46. |
| DUTY-OT-Y ≤ 960h/năm, công thức chưa có (OQ-58) | #{I-0807} | Là STUB (k = 1.25); tách để không kéo cả validator vào trạng thái chờ. |
| Vi phạm thì cấm công bố, hiện đúng khoảng vi phạm, không có nút override (T-13) | #{I-0808} API + panel/timeline; #{I-0809} cổng công bố | Hiển thị (không +1 pháp lý) tách khỏi cổng công bố (transaction, gắn version, không hồi tố). |
| Tuyến gắn version quy tắc lúc công bố, không áp hồi tố (FR-SCH-04, T-16) | #{I-0809} | Kiểm lại trong transaction và xử lý `RULE_VERSION_CHANGED` là rủi ro kỹ thuật riêng. |
| Giờ thực tế tài xế (P-09, OQ-32) | #{I-0810} SCR-063 | Màn chưa có spec ở LAB-4 (PREMISE S-01). |
| Sự cố bất khả kháng tách khỏi tuân thủ (FR-SCH-05, T-17) | #{I-0811} SCR-062; #{I-0812} 2 báo cáo tách | RFP yêu cầu 2 báo cáo riêng, không ghi đè kết quả tuân thủ. |
| Nghiệm thu ACC-SCH-01 | #{I-0813} bộ test biên | Bằng chứng nghiệm thu; QA làm song song với dev, không nằm trong DoD từng issue. |
| (kéo theo) Dỡ đơn ở G4 → version tuyến mới → kiểm giờ lại | #{I-0604} | Nghiệp vụ F06 nhưng phải chạy lại validator; reviewer tăng SWP 8 → 13 vì lý do này. |
| (kéo theo) Revision/hủy tuyến | #{I-0704} | Mỗi revision phải kiểm giờ lại trước khi công bố lại. |
| (kéo theo) Tài xế chỉ nhận bản mới nhất có điểm nghỉ | #{I-0901} | PWA thuộc F07 (PREMISE D-05). |

**Ảnh hưởng tới break task và estimate:** 13 issue / 90 SWP / 371 giờ ở E08, gồm 8 issue +1 Complexity pháp lý. So với LAB-1, phần này **tăng khoảng 44%** (estimate.md §4), trong khi các epic khác giảm vì còn thô. Sprint 1 ưu tiên E08 (#{I-0801}, #{I-0802}, #{I-0803}) vì đây là đường găng có rủi ro chờ khách.

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi break

| Spec | Chỗ hở/mâu thuẫn | Xử lý |
|---|---|---|
| F08 P-09, FT-08-06 | SCR-063 được nhắc tên nhưng không có spec/wireframe/API, trong khi validator cần giờ thực tế D−1 | Đã sửa thiết kế: PREMISE S-01 → #{I-0810} |
| business-rules DSG-DUTY-01 | DUTY-DRV-2D: thiết kế chọn BOTH nhưng ghi tranh chấp với reviewer (EITHER) | Đã sửa thiết kế: PREMISE S-02, hướng chốt D-01 → #{I-0805} |
| F08 technical-spec FR-SCH-05 | SCR-062 "chưa có spec"; chỉ có API contract | Đã sửa thiết kế: PREMISE S-03 → #{I-0811} |
| business-rules DUTY-OT-Y | Có ngưỡng 960h nhưng chưa có công thức giờ làm thêm (OQ-58) | Tạo issue làm rõ #{I-0802} (phần làm: STUB theo PREMISE S-05, #{I-0807}) |
| business-rules §E, OQ-30 | Chưa mô hình hóa ngoại lệ 告示 (310h, 14h × 2/tuần, nghỉ chia đôi, đường dài) | Để mở: chưa biết khách có áp dụng; nếu có sẽ thêm issue vào E08. Đã hỏi trong #{I-0802} |
| F08 US-484 ↔ F07 | "Tài xế chỉ nhận bản mới nhất" thuộc F08 nhưng màn PWA thuộc F07 (mức kiến trúc) | Đã sửa thiết kế: PREMISE D-05 → #{I-0901} |
| architecture §4 IF-MAP-01 | Chưa có nhà cung cấp bản đồ → không test được ETA và luật 24h | Đã sửa thiết kế: PREMISE S-06 → #{I-0702} |
| F09 BR-HACCP-01 ↔ FIG-010 | Mâu thuẫn: cách ly ngay vs đo lại 15 phút / 保留 (OQ-56) | Để mở và vì sao: mâu thuẫn ngay trong RFP, phải để khách quyết; tạm làm theo BR-HACCP-01 (PREMISE D-03) |
| F06 SM-801 | PUBLISHED → IN_PROGRESS do F06 sở hữu nhưng khóa revision thuộc F08; thứ tự triển khai chưa rõ | Giả định: PREMISE A-07 |
| prototype-vs-design G-32 | Seed SKU prototype lệch RFP R-02 (CHI-001 là gà thay vì bò) | Giả định: PREMISE A-08 (#{I-0201}) |
| feature-list "khoảng trống" | FR-INV-04, FORM-REC-01, HACCP completeness chưa có màn | Tạo issue làm rõ (thiết kế) #{I-0406}, #{I-0306}, #{I-1006} |
