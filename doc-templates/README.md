# LAB-5 — Backlog, GitHub Project và báo cáo tiến độ · Product B

**Dự án:** Yuki Cold Logistics — hệ thống chuỗi kho lạnh thực phẩm · **Mã học viên:** haiht-1795 · **Đề:** Product B

## Tổng quan

- **Backlog break từ:** bộ thiết kế LAB-4 `lab 4-AIDD` (nộp 2026-11-14): 7 feature thiết kế sâu (F02 phần chính sách, F03, F04, F05, F06, F08, F09), 10 screen spec + wireframe, 9 ADR, 27 dòng truy vết ràng buộc. Các feature còn lại lấy ở mức kiến trúc/dữ liệu.
- **PREMISE.md có thay đổi:** có. 6 thay đổi spec (S-01…S-06, chủ yếu ở phần giờ lái 2024), 8 giả định (A-01…A-08), 5 hướng chốt (D-01…D-05).
- **Số epic:** 14 (F01…F13; F08 tách 2 epic, trong đó **E08 dành riêng cho giới hạn giờ lái xe tải 2024 — 改善基準告示**). 80 issue, 91 sub-issue, 482 SWP, 2.008 giờ.
- **Sprint giả lập đã chạy:** Sprint 1 (2026-11-16 → 2026-11-27): cam kết 66 SWP, xong 32 SWP. Sprint 2 và 3 mới xếp sơ bộ.

## Link

- Repo: https://github.com/haiht-1795/lab5-product-b-backlog
- GitHub Project: https://github.com/users/haiht-1795/projects/1
- Báo cáo HTML của skill chấm SWP: [reports/swp-report.html](reports/swp-report.html) (xem render: https://htmlpreview.github.io/?https://github.com/haiht-1795/lab5-product-b-backlog/blob/main/reports/swp-report.html)
- Đã mở thử repo, Project và báo cáo HTML bằng cửa sổ ẩn danh (không đăng nhập): xem được cả ba.

## Cấu trúc repo

| File/thư mục | Nội dung |
|---|---|
| `README.md` | File này |
| `PREMISE.md` | Backlog khác LAB-4 ở đâu: spec thêm/bỏ/sửa, giả định, hướng chốt |
| `task-breakdown.md` | Nguyên tắc chia task, Spec → issue, hạng mục giờ lái 2024, chỗ hở của spec |
| `estimate.md` | Issue mẫu skill chọn + quyết định review, quy ước đổi giờ, tổng theo epic, so với LAB-1 |
| `progress-report.md` | Báo cáo Sprint 1: trạng thái, burndown, rủi ro trễ |
| `AI-report.md` | Cách dùng AI, cách review, điểm tốt/chưa tốt |
| `reports/` | Thư mục tự đặt: `swp-report.html` (báo cáo HTML của skill chấm SWP), `burndown-sprint-1.svg` + bảng burndown |
| `skills/` | `swp-scoring/`: skill chấm SWP tự viết (SKILL.md + script) |
| `backlog/` | Dữ liệu nguồn: `backlog.json` (backlog), `swp-review.json` (quyết định review), `backlog-scored.json` (kết quả skill), `lab1-estimate.json` (man-day LAB-1), `sprint-1-daily-log.json`, `github-map.json` (khóa → số issue) |
| `scripts/` | Đồng bộ issue/Project, vẽ burndown, render bảng vào tài liệu |
| `doc-templates/` | Bản nguồn của 6 file Markdown ở gốc (bảng và số issue do script điền) |

Chạy lại toàn bộ: `swp-score.py` → `github-issues-sync.py` → `github-project-sync.py` → `burndown-chart-svg.py` → `render-doc-tables.py` (lệnh đầy đủ ở đầu mỗi script).

## Spec → epic

{{TABLE:epic-map}}
