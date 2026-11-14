# Báo cáo tiến độ — Sprint 1 (giả lập)

- **Iteration trên Project:** `Sprint 1` (trường Iteration của [GitHub Project](https://github.com/users/haiht-1795/projects/1))
- **Khoảng thời gian giả lập:** 2026-11-16 → 2026-11-27 (10 ngày làm việc). Ngày báo cáo: 2026-11-27.
- **Gửi:** Yuki Cold Logistics — bộ phận phụ trách dự án. Dữ liệu trạng thái là giả lập (PREMISE A-03).

## Tóm tắt cho khách

Sprint 1 dựng xong nền tảng kỹ thuật và màn quản lý phiên bản quy tắc giờ lái 2024 (SCR-017). Hoàn thành **32/66 SWP (48%)**. Hai việc lớn phải chuyển sang Sprint 2: module quy tắc hạn dùng/phân bổ và mô hình timeline tài xế.
Việc cần khách hỗ trợ gấp: **trả lời OQ-28, OQ-29, OQ-30, OQ-58 và cử người xác minh pháp lý cho 改善基準告示**. Đây là đường găng của mốc demo kiểm giờ lái (cuối Sprint 3, 2026-12-25).

## 1. Trạng thái

| Trạng thái | Số issue | Tổng SWP | Giờ | Ghi chú |
|---|---:|---:|---:|---|
| Done | 6 | 32 | 128 | #15, #16, #22, #25, #31, #102 |
| In Review | 1 | 5 | 20 | #17 |
| In Progress | 2 | 26 | 104 | #58, #106 |
| Blocked | 1 | 3 | 15 | #105 |
| **Cam kết** | **10** | **66** | **267** | |

Ghi chú:
- #17 (OIDC + MFA) xong code nhưng chờ khách cấp tenant IdP test có MFA nên chưa nghiệm thu được.
- #58: 2/4 sub-issue xong; phần mốc đảo ngày (dateReversal) đang làm.
- #106: 1/4 sub-issue xong; chia ngày cho tuyến qua đêm khó hơn dự kiến.
- #105 Blocked: khách chưa có người chịu trách nhiệm xác minh pháp lý; chưa có trả lời 4 OQ.

## 2. Burndown

![Burndown Sprint 1](reports/burndown-sprint-1.svg)

| Ngày | SWP lý tưởng | SWP còn lại | Giờ còn lại | Hoàn thành trong ngày | Ghi chú |
|---|---:|---:|---:|---|---|
| 2026-11-16 | 66.0 | 66 | 267 | — | Sprint planning: cam kết 10 issue / 66 SWP / 267 giờ |
| 2026-11-17 | 58.7 | 63 | 255 | #15 | Khung monorepo + CI xong |
| 2026-11-18 | 51.3 | 60 | 243 | #25 | Gửi OQ-28/29/30/58 cho khách qua BrSE |
| 2026-11-19 | 44.0 | 60 | 230 | #59 | #105 chuyển Blocked: khách chưa có người xác minh pháp lý |
| 2026-11-20 | 36.7 | 55 | 194 | #31, #23 |  |
| 2026-11-23 | 29.3 | 50 | 161 | #16, #107 | Phát hiện tuyến qua đêm làm #108 khó hơn dự kiến |
| 2026-11-24 | 22.0 | 50 | 132 | #103, #60 | IdP test tenant của khách chưa cấp MFA → #17 chờ |
| 2026-11-25 | 14.7 | 42 | 116 | #24, #22 |  |
| 2026-11-26 | 7.3 | 34 | 100 | #104, #102 | SCR-017 hiển thị banner 法務未確認 đúng spec |
| 2026-11-27 | 0.0 | 34 | 100 | — | Review: #17 còn 2 comment; #58, #106 chuyển tiếp Sprint 2 |

Cam kết: 66 SWP / 267 giờ.

**Thực tế lệch kế hoạch ở đâu**
- **Cam kết quá sức.** 66 SWP / 267 giờ là ~76% năng lực lý thuyết (≈ 350 giờ). Nhưng ngay sprint đầu đã có hai issue 13 SWP, mà một issue 13 SWP chỉ tính là xong khi cả 4 sub-issue xong. Đường thực tế đi ngang 3 ngày (19/11, 24/11, 27/11) dù giờ vẫn giảm: sub-issue xong nhưng issue cha chưa xong.
- **Giờ đốt tốt hơn SWP:** còn 100/267 giờ (63% đã làm) nhưng còn 34/66 SWP (48% đã làm). Việc vẫn tiến, chỉ chưa đóng được issue. Từ Sprint 2, issue 13 SWP phải được chia để đóng trong sprint, hoặc không nhận quá 1 issue 13 SWP/người.
- **Chờ khách:** #105 bị chặn từ ngày thứ 4 (19/11); #17 chờ tenant IdP. Hai việc này không do đội, nhưng chiếm 8 SWP chưa đóng.
- **Kế hoạch Sprint 2 phải cắt.** Bản xếp sơ bộ Sprint 2 trên Project là 15 issue / 99 SWP, cộng 34 SWP chuyển tiếp. Với tốc độ 32 SWP/sprint, sẽ cắt còn ≈ 45 SWP ở buổi planning ngày 2026-11-30 (R-04).

## 3. Rủi ro trễ tiến độ

| # | Rủi ro | Issue | Ảnh hưởng tới mốc nào | Hành động | Ai làm, khi nào |
|---|---|---|---|---|---|
| R-01 | Khách chưa trả lời OQ-28/29/30/58 và chưa có người xác minh 改善基準告示 | #105, #111, #114, #118 | M-DUTY: demo kiểm giờ lái + công bố tuyến (cuối Sprint 3, 2026-12-25); UAT kịch bản ACC-SCH-01 | Làm theo tham số (BOTH/EITHER, công thức OT là strategy) để không chặn code; đưa 4 OQ vào họp steering, đề nghị hạn trả lời 2026-12-04; version quy tắc giữ `verified_by_legal = false` | BrSE gửi lại + PM nêu ở steering 2026-12-01; khách trả lời trước 2026-12-04 |
| R-02 | Chia ngày cho tuyến qua đêm (DSG-DUTY-03) khó hơn ước lượng | #106 | M-DUTY | Pair BE2 + TL 2 ngày đầu Sprint 2; viết trước test biên của #133 cho phần chia ngày | TL, 2026-11-30 → 12-01 |
| R-03 | Chưa chọn nhà cung cấp bản đồ (OQ-35) | #92, #95, #125 | M-DUTY (luật cấm công bố khi ước tính > 24h không test được) | Dùng fake provider (PREMISE S-06); xin quyết định nhà cung cấp trước Sprint 3 | PM hỏi khách 2026-12-01; TL xong fake provider trong Sprint 3 |
| R-04 | Cam kết sprint vượt tốc độ thực (66 cam kết, 32 xong) | toàn Sprint 2 | Mọi mốc sau nếu không cắt | Planning Sprint 2 đặt trần ≈ 45 SWP = tốc độ thực 32 SWP + ≈ 13 SWP dự phòng (2 issue chuyển tiếp đã làm hơn nửa giờ); issue mới chỉ nhận trong phần còn lại; hạ ưu tiên #18, #21, #34 | TL + PM, planning 2026-11-30 |
| R-05 | Tenant IdP test có MFA chưa được cấp | #17, #18 | Mốc demo nội bộ Sprint 2 (đăng nhập theo vai trò) | Dùng IdP giả lập (OIDC mock) cho test; nghiệm thu thật khi có tenant | SYS phía khách cấp trước 2026-12-04; BE2 dựng mock 2026-11-30 |
| R-06 | Estimate LAB-5 thấp hơn LAB-1 ≈ 45% vì nhiều phần chưa issue hóa (F07, F10–F13, màn List) | #27, #47, #57, #165, epic #9, #11, #12, #14 | Mốc tổng (go-live) nếu dùng nhầm số LAB-5 để lập lịch | Không cắt ngân sách theo số LAB-5; spec các phần thiếu theo thứ tự ưu tiên, estimate lại khi đóng spec | BrSE + TL, spec F07 trước 2026-12-11 |
| R-07 | Mâu thuẫn RFP về cách ly sau alarm (OQ-56) | #160 | Mốc giám sát nhiệt (sau Sprint 3) | Làm theo BR-HACCP-01 (PREMISE D-03); hỏi khách cùng R-01 | BrSE, 2026-12-01 |
