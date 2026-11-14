---
name: swp-scoring
description: Chấm SWP (Scope × Complexity → SWP) cho backlog JSON, quy SWP ra giờ theo quy ước cố định, kiểm độ hạt task, chọn issue mẫu cho người review và xuất báo cáo HTML. Dùng khi break task xong và cần estimate có thể kiểm lại.
---

# swp-scoring — chấm SWP cho backlog

Skill do học viên tự viết cho LAB-5 (không có skill chấm SWP chính thức trên máy).
Mục tiêu: điểm số **tái lập được** (cùng input → cùng SWP), có chỗ để **người** sửa, và giữ vết lý do sửa.

## Input

- `backlog/backlog.json`: mỗi issue có `S` (Scope 1–5), `C` (Complexity 1–5), `legal` (bool), `oqMode` (`""`/`CFG`/`STUB`/`BLOCK`), `subs` (sub-issue và tỉ lệ giờ).
- `backlog/swp-review.json` (tùy chọn): quyết định của người review `{ "I-xxxx": {"S":..,"C":..,"note":".."} }`.

## Thang chấm

| Điểm | Scope (độ rộng) | Complexity (độ khó) |
|---|---|---|
| 1 | 1 trường/hàm | CRUD thuần |
| 2 | 1 endpoint hoặc 1 component | validation chuẩn |
| 3 | 1 use case qua API + UI, hoặc 1 module quy tắc | state machine, maker-checker |
| 4 | nhiều use case / 1 màn nhiều trạng thái | transaction, đồng thời, quy tắc nghiệp vụ có biên |
| 5 | luồng xuyên module | offline + mã hóa, tích lũy nhiều ngày/tháng |

- **Cộng +1 Complexity (tối đa 5)** khi `legal = true`: ngưỡng lấy từ luật/tiêu chuẩn **chưa xác minh** (OPS-LAW-01, ví dụ 改善基準告示 2024). Lý do: phải viết thành tham số có version, test ranh giới “bằng giới hạn / vượt 1 phút”, và chịu rủi ro đổi cách hiểu.
- `SWP = Fib(S × C)`: ≤2→1 · 3–4→2 · 5–6→3 · 8–10→5 · 12→8 · 15–16→13 · ≥20→21.

## Quy ước đổi giờ

`Giờ = SWP × 4h × k`; `k = 1.25` nếu `oqMode ∈ {STUB, BLOCK}` (phần làm theo đề xuất tạm, dễ phải làm lại), ngược lại `k = 1`. Làm tròn đến giờ.

## Kiểm độ hạt (flag)

| Mã | Điều kiện | Ý nghĩa |
|---|---|---|
| SPLIT | SWP = 21 | Quá lớn → phải tách thành nhiều issue |
| NEED-SUB | giờ > 24 mà không có sub-issue | Phải tách sub-issue |
| SUB-BIG | sub-issue > 16h | Sub-issue quá lớn |
| BLOCK-SPRINT | `oqMode = BLOCK`, không phải issue làm rõ/thiết kế, lại được xếp sprint | Xếp việc chưa làm được |
| DESIGN-SPRINT | `needsDesign` mà được xếp sprint | Làm trước khi có spec |

## Chọn issue mẫu cho người review

1. Mọi issue có flag.
2. Issue `legal` có SWP ≥ 8 (ràng buộc đặc thù, sai là sai cả epic).
3. Issue chấm lệch (|S − C| ≥ 2): dễ đánh giá sai một chiều.
4. Issue SWP lớn nhất mỗi epic chưa được chọn ở bước 1–3 (đối chứng).

## Chạy

```bash
python skills/swp-scoring/scripts/swp-score.py backlog/backlog.json backlog/swp-review.json \
  --out backlog/backlog-scored.json --html reports/swp-report.html
```

Sau khi người review ghi quyết định vào `swp-review.json`, chạy lại. Báo cáo HTML hiện cả điểm skill và điểm chốt.
Ghi lên GitHub Project bằng `scripts/github-project-sync.py` (đọc `backlog-scored.json`).
