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

| Spec | Epic | Issue / sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| architecture.md §1–3, §6; ADR-001/002/008; permissions-matrix.md | #1 | #15 ADR-001; architecture.md §3<br>#16 ADR-001; architecture.md §7<br>#17 FT-01-01, FT-01-02; ADR-008; IF-IDP-01<br>#18 FT-01-03; permissions-matrix.md; T-23 (2 sub)<br>#21 FT-01-04; ADR-008; NFR-SEC-02<br>#22 FT-01-06; NFR-AUD-01; ADR-002; T-22; G-22 (2 sub)<br>#25 architecture.md §6<br>#26 FT-01-07; IF-MAIL-01<br>#27 FT-01-05, FT-01-08, FT-01-09 (chưa có spec chi tiết) | Màn đăng nhập/khóa phiên (mức List) gộp trong #27 chờ spec. NFR hiệu năng, BCP, quét bảo mật là hạng mục cố định của LAB-1, không phải issue dev. |
| F02-policy-versioning; SCR016; ADR-003; prototype-vs-design G-01/02/07/23/32 | #2 | #28 FT-02-01, FT-02-03, FT-02-04, FT-02-05; G-01, G-02, G-07, G-23, G-32<br>#29 FT-02-08; erd.md vehicle, vehicle_compartment, driver; DR-PRIV-01<br>#30 FT-02-09; DR-MST-01<br>#31 ADR-003; F02 technical-spec Algorithms; T-01<br>#32 SCR016_TempPolicyVersion; wireframes/SCR016; BR-TEMP-01; T-01<br>#33 FT-02-02; DISC-022; US-473; G-20<br>#34 FT-02-10 | Các màn master mức List (SCR-010…015) chưa issue riêng: CRUD theo mẫu, issue hóa khi có spec màn. Ngưỡng nhiệt riêng SKU (OQ-25) chưa thành issue vì RFP không yêu cầu. |
| F03-inbound-inspection; SCR021; SCR022; T-02/T-03 | #3 | #35 SCR021_InboundInspection; FT-03-02; US-01; T-02; G-08 (4 sub)<br>#40 FT-03-05; FR-REC-05; T-03; DSG-REC-02<br>#41 FT-03-07; BR-TRACE-01/02<br>#42 FT-03-03; US-410; PERM003<br>#43 SCR022_InboundConfirm; FT-03-04; US-411 (3 sub)<br>#47 FT-03-01, FT-03-06; feature-list.md khoảng trống | Đo lại trong 15 phút / trạng thái 保留 (OQ-56, mâu thuẫn RFP) chưa thành issue. Phần làm SCR-020/023 chỉ có issue thiết kế #47. |
| F04-inventory-quarantine; SCR034; T-04/T-05/T-11c | #4 | #48 FT-04-02, FT-04-03; US-422; G-09 (4 sub)<br>#53 SCR034_QuarantineJudgement; US-03; T-05; G-12<br>#54 DSG-QUA-01; T-04<br>#55 DSG-QUA-03; T-11c; G-33<br>#56 FT-04-01, FT-04-05<br>#57 FT-04-04; FR-INV-04 | Kiểm kê mù chỉ có issue thiết kế #57; vị trí -Q đầy (OQ-48) xử lý STUB trong #54. |
| F05-allocation; SCR042; ADR-004/005; T-06…T-10 | #5 | #58 FT-05-02, FT-05-03, FT-05-04; T-06/T-07/T-08; ALG-502/503 (4 sub)<br>#63 DSG-ALLOC-01; BR-FEFO-01; T-09<br>#64 ADR-004; FR-OUT-02; T-10; G-05, G-10 (2 sub)<br>#67 SCR042_AllocationResult; FT-05-06<br>#68 DSG-ALLOC-04; US-402<br>#69 FT-05-01; SCR-040/041 (mức List) | Đơn con backorder (OQ-08 BLOCK) chưa có mô hình; cảnh báo sớm phân bổ trùng cặp KH–SKU (OQ-11) để sau. |
| F06-outbound-check; SCR051; SCR053; T-11/T-11b/T-12 | #6 | #70 SCR051_PickLoadScan; FT-06-02; T-11; G-14, G-27 (4 sub)<br>#75 SCR053_PreShipCheck; FR-OUT-05; T-12; G-15<br>#76 ALG-603, ALG-605; ADR-005; G-28, G-29 (2 sub)<br>#79 ALG-604; DSG-ALLOC-05; T-11b (5 sub)<br>#85 FT-06-01; FR-OUT-03 (SCR-050 mức List)<br>#86 FT-06-04; PREMISE LAB-4 C-2 | Tái kiểm sau FAIL kiểm trước xuất (OQ-61) làm bằng CFG trong #75; deviation do chênh nhiệt tài xế/WHL (OQ-55) chưa thiết kế. |
| F08-route-duty-hours (ALG-801, SM-801, DEC-802/803); SCR060 phần stop/xe; T-18 | #7 | #87 ALG-801; FR-SCH-01; US-480; T-18 (4 sub)<br>#92 IF-MAP-01; DSG-ROUTE-01; P-10 (2 sub)<br>#95 SCR060_RoutePlanning (phần stop); wireframes/SCR060 (4 sub)<br>#100 SM-801; DEC-803; FR-SCH-04 (phần version)<br>#101 DEC-802; US-486; DR-PRIV-01 | Phân loại/báo cáo làm thêm có kế hoạch (OQ-64) chưa thiết kế; tối ưu tuyến tự động (VRP) không có trong RFP. |
| F08 FR-SCH-02/03/05, DSG-DUTY-01/02/03; SCR017; SCR060 panel kiểm giờ; ADR-006; T-13…T-17 | #8 | #102 SCR017_DutyRuleSetVersion; FT-02-07; DISC-023; US-471; T-14 (2 sub)<br>#105 OPS-LAW-01; open-questions OQ-28, OQ-29, OQ-30, OQ-58<br>#106 DSG-DUTY-03; ADR-006; business-rules §E (4 sub)<br>#111 FR-SCH-02; business-rules DUTY-BIND-*, DUTY-REST (2 sub)<br>#114 DSG-DUTY-01; PREMISE LAB-5 S-02, D-01<br>#115 FR-SCH-03; DSG-DUTY-02; US-482; T-15 (2 sub)<br>#118 business-rules DUTY-OT-Y; OQ-58 (2 sub)<br>#121 US-481; T-13; SCR060 §Validation; SM-802 (3 sub)<br>#125 DEC-801; SM-801 CHECKED→PUBLISHED; FR-SCH-04; T-13, T-16 (4 sub)<br>#130 FT-08-06; P-09; PREMISE LAB-5 S-01<br>#131 FR-SCH-05; F08 API contract FM1–FM9; US-485; T-17; PREMISE LAB-5 S-03<br>#132 FR-SCH-05; US-487<br>#133 ACC-SCH-01; T-13…T-17; PREMISE LAB-5 S-04 (4 sub) | Ngoại lệ 告示 (310h/tháng, 14h tối đa 2 lần/tuần, nghỉ chia đôi, đường dài, 2 tài xế, phà; OQ-30 BLOCK) chưa thành issue vì chưa biết khách có áp dụng. Tích hợp tachograph (upsale P2, OQ-32) ngoài phạm vi. |
| ADR-009; feature-list F07 (mức kiến trúc) | #9 | #138 FT-07-01; US-484; ADR-009 (2 sub)<br>#141 FT-07-02; BR-POD-01; G-19 (3 sub)<br>#145 FT-07-03; ADR-009; NFR-AVL-02; T-24 (5 sub)<br>#151 FT-07-04, FT-07-05 (2 sub) | Spec chi tiết F07 (SCR-070…072) chưa có ở LAB-4 → mọi issue gắn needs-design, ước lượng thô. |
| F09-temperature-monitoring; SCR082; ADR-007; T-19…T-21b | #10 | #154 FT-09-01; FR-TEMP-01; ADR-007; T-19 (2 sub)<br>#157 FT-09-02; FR-TEMP-02; DSG-TEMP-02; T-20 (2 sub)<br>#160 BR-HACCP-01; DSG-TEMP-04; T-21b; G-31 (2 sub)<br>#163 SCR082_TempAlarmQueue; FR-TEMP-03; T-21<br>#164 FT-09-04; US-495<br>#165 FT-09-05…07; BR-HACCP-01 | Đo lại 15 phút/保留 (OQ-56) như E03. HACCP chi tiết chờ #165. |
| feature-list F10 (mức dữ liệu: delivery_line, lot) | #11 | #166 FT-10-01; FR-TRC-01<br>#167 FT-10-02, FT-10-03 (2 sub) | Spec màn F10 chưa có (LAB-4 chỉ ở mức dữ liệu): 2 issue thô. |
| feature-list F11 (mức kiến trúc: read replica, manifest) | #12 | #170 FT-11-01 (phần kho) (2 sub)<br>#173 FT-11-01 (phần xuất, nhiệt)<br>#174 FT-11-02<br>#175 FT-11-03, FT-11-04; FR-RPT-02 | 12 báo cáo chưa có spec từng báo cáo → tạm chia 6 + 6. |
| architecture.md §4 | #13 | #176 FT-12-01; IF-ERP-01; P-24<br>#177 FT-12-01, FT-12-03; IF-ARCH-01<br>#178 FT-12-04; NFR-OPS-01 | Tích hợp bản đồ chuyển sang E07 (#92) vì gắn với luật cấm công bố khi ước tính > 24h. |
| feature-list F13 (mức nguyên tắc ACCEPT/REJECT/DUPLICATE/BUSINESS-REVIEW) | #14 | #179 FT-13-01; DR-MIG-01 (2 sub)<br>#182 FT-13-02<br>#183 FT-13-03; DSG-DATE-01; G-24 (2 sub) | Workshop mapping, dry run, rehearsal (hạng mục cố định LAB-1, 67 MD) là hoạt động dự án, không phải issue dev. |

## 3. Hạng mục chịu ràng buộc đặc thù: giới hạn giờ lái xe tải từ 2024 (改善基準告示)

Toàn bộ nằm ở epic #8 (nhãn `constraint:duty-2024`, trường `Ràng buộc đặc thù = Giờ lái 2024`). Ba issue ở epic khác bị ràng buộc kéo theo, gắn `constraint:touch-duty-2024`.

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Ngưỡng luật là bản tóm tắt, phải xác minh với nguồn chính thức (OPS-LAW-01, T-14) | #102 SCR-017 version quy tắc + cờ `verified_by_legal`; #105 làm rõ pháp lý với khách | Là nơi duy nhất giữ giá trị luật. Có rủi ro chờ khách (BLOCK) khác hẳn việc dev, nên tách issue làm rõ để theo dõi riêng trên board. |
| Định nghĩa "1 ngày" = 24h từ đầu ca, gộp nhiều tuyến/ngày, giờ thực tế D−1 (DSG-DUTY-03, OQ-29) | #106 timeline tài xế | Mọi mã DUTY-* dùng chung mô hình này; sai ở đây thì sai cả 8 mã. Tách ra để làm và review trước. |
| DUTY-BIND-D/M/Y 13–15h / 284h / 3.300h, DUTY-REST 11h/9h | #111 | Cùng cơ chế tích lũy ngày/tháng/năm. Gộp lại với 2D/2W thì vượt 13 SWP (skill flag SPLIT). |
| DUTY-DRV-2D (BOTH/EITHER còn tranh chấp), DUTY-DRV-2W 44h × 2 tuần | #114 | Phụ thuộc OQ-28; tách để nếu khách đổi cách đọc chỉ đổi đúng issue này (PREMISE S-02, D-01). |
| DUTY-CONT ≤ 4h + tự chèn nghỉ 30 phút / ≥ 10 phút (FR-SCH-03) | #115 | Vừa là kiểm vừa sinh dữ liệu (BREAK auto_inserted); phụ thuộc OQ-31, OQ-46. |
| DUTY-OT-Y ≤ 960h/năm, công thức chưa có (OQ-58) | #118 | Là STUB (k = 1.25); tách để không kéo cả validator vào trạng thái chờ. |
| Vi phạm thì cấm công bố, hiện đúng khoảng vi phạm, không có nút override (T-13) | #121 API + panel/timeline; #125 cổng công bố | Hiển thị (không +1 pháp lý) tách khỏi cổng công bố (transaction, gắn version, không hồi tố). |
| Tuyến gắn version quy tắc lúc công bố, không áp hồi tố (FR-SCH-04, T-16) | #125 | Kiểm lại trong transaction và xử lý `RULE_VERSION_CHANGED` là rủi ro kỹ thuật riêng. |
| Giờ thực tế tài xế (P-09, OQ-32) | #130 SCR-063 | Màn chưa có spec ở LAB-4 (PREMISE S-01). |
| Sự cố bất khả kháng tách khỏi tuân thủ (FR-SCH-05, T-17) | #131 SCR-062; #132 2 báo cáo tách | RFP yêu cầu 2 báo cáo riêng, không ghi đè kết quả tuân thủ. |
| Nghiệm thu ACC-SCH-01 | #133 bộ test biên | Bằng chứng nghiệm thu; QA làm song song với dev, không nằm trong DoD từng issue. |
| (kéo theo) Dỡ đơn ở G4 → version tuyến mới → kiểm giờ lại | #79 | Nghiệp vụ F06 nhưng phải chạy lại validator; reviewer tăng SWP 8 → 13 vì lý do này. |
| (kéo theo) Revision/hủy tuyến | #100 | Mỗi revision phải kiểm giờ lại trước khi công bố lại. |
| (kéo theo) Tài xế chỉ nhận bản mới nhất có điểm nghỉ | #138 | PWA thuộc F07 (PREMISE D-05). |

**Ảnh hưởng tới break task và estimate:** 13 issue / 90 SWP / 371 giờ ở E08, gồm 8 issue +1 Complexity pháp lý. So với LAB-1, phần này **tăng khoảng 44%** (estimate.md §4), trong khi các epic khác giảm vì còn thô. Sprint 1 ưu tiên E08 (#102, #105, #106) vì đây là đường găng có rủi ro chờ khách.

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi break

| Spec | Chỗ hở/mâu thuẫn | Xử lý |
|---|---|---|
| F08 P-09, FT-08-06 | SCR-063 được nhắc tên nhưng không có spec/wireframe/API, trong khi validator cần giờ thực tế D−1 | Đã sửa thiết kế: PREMISE S-01 → #130 |
| business-rules DSG-DUTY-01 | DUTY-DRV-2D: thiết kế chọn BOTH nhưng ghi tranh chấp với reviewer (EITHER) | Đã sửa thiết kế: PREMISE S-02, hướng chốt D-01 → #114 |
| F08 technical-spec FR-SCH-05 | SCR-062 "chưa có spec"; chỉ có API contract | Đã sửa thiết kế: PREMISE S-03 → #131 |
| business-rules DUTY-OT-Y | Có ngưỡng 960h nhưng chưa có công thức giờ làm thêm (OQ-58) | Tạo issue làm rõ #105 (phần làm: STUB theo PREMISE S-05, #118) |
| business-rules §E, OQ-30 | Chưa mô hình hóa ngoại lệ 告示 (310h, 14h × 2/tuần, nghỉ chia đôi, đường dài) | Để mở: chưa biết khách có áp dụng; nếu có sẽ thêm issue vào E08. Đã hỏi trong #105 |
| F08 US-484 ↔ F07 | "Tài xế chỉ nhận bản mới nhất" thuộc F08 nhưng màn PWA thuộc F07 (mức kiến trúc) | Đã sửa thiết kế: PREMISE D-05 → #138 |
| architecture §4 IF-MAP-01 | Chưa có nhà cung cấp bản đồ → không test được ETA và luật 24h | Đã sửa thiết kế: PREMISE S-06 → #92 |
| F09 BR-HACCP-01 ↔ FIG-010 | Mâu thuẫn: cách ly ngay vs đo lại 15 phút / 保留 (OQ-56) | Để mở và vì sao: mâu thuẫn ngay trong RFP, phải để khách quyết; tạm làm theo BR-HACCP-01 (PREMISE D-03) |
| F06 SM-801 | PUBLISHED → IN_PROGRESS do F06 sở hữu nhưng khóa revision thuộc F08; thứ tự triển khai chưa rõ | Giả định: PREMISE A-07 |
| prototype-vs-design G-32 | Seed SKU prototype lệch RFP R-02 (CHI-001 là gà thay vì bò) | Giả định: PREMISE A-08 (#28) |
| feature-list "khoảng trống" | FR-INV-04, FORM-REC-01, HACCP completeness chưa có màn | Tạo issue làm rõ (thiết kế) #57, #47, #165 |
