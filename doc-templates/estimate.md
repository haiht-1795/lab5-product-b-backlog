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

{{TABLE:samples}}

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

{{TABLE:epic-totals}}

## 4. So với estimate LAB-1

LAB-1 ước man-day (8h) cho phần **build FE + BE + UT** của 74 tính năng, cộng 25 MD dựng platform, tổng 610 MD. Các pha thiết kế, IT, ST, UAT, migration, đào tạo, PM được tính theo tỉ lệ và hạng mục cố định ngoài con số này. Vì vậy chỉ so phần build. Giờ LAB-5 quy ra MD theo **6 giờ tập trung/ngày** (cùng cơ sở với năng lực sprint), không chia 8. Tính năng LAB-1 xuất hiện ở nhiều epic (FT-08-04) được chia đều.

{{TABLE:lab1-compare}}

**Đọc bảng:**
- **Epic có ràng buộc đặc thù (E08) tăng khoảng 44%.** Đây là phần được break kỹ nhất. Ràng buộc 2024 làm phát sinh việc LAB-1 chưa thấy: tách validator, test biên, 2 màn thiếu spec, cổng công bố trong transaction (PREMISE S-01…S-05).
- **E06, E07 gần khớp.** Hai epic này có spec chi tiết ở LAB-4 và không có tính năng chờ thiết kế.
- **Các epic khác thấp hơn 48–73%, không phải vì làm nhanh hơn.** Phần lớn chênh đến từ chỗ chưa issue hóa: màn mức List, F07/F10–F13 chỉ có issue thô `needs-design`, các tính năng mới có issue thiết kế. Một phần nhỏ đến từ tái dùng module quy tắc của prototype.
- **Kết luận:** tổng LAB-5 (≈ 335 MD) **chưa thay được** con số LAB-1 để báo giá hay đổi mốc. Khi spec các phần còn thiếu xong, estimate sẽ tăng lại. Rủi ro này được theo dõi ở progress-report.md (R-06).
