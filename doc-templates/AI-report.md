# AI-report — Dùng AI trong LAB-5

Công cụ: Claude Code (Claude Opus 5.5) chạy trong VS Code, có quyền đọc thư mục LAB-1/LAB-4 trên máy và dùng `gh` CLI (scope `repo`, `project`).

## 1. Skill và prompt cho từng việc

| Việc | Skill / công cụ | Prompt và cách giao việc |
|---|---|---|
| Đọc input | Đọc file trực tiếp (Read/Grep), không dùng subagent | Dán nguyên đề LAB-5. AI tự đọc LAB-4 theo thứ tự README LAB-4 gợi ý: PREMISE → feature-list → constraint-traceability → F08 business-context/technical-spec → open-questions (cột Dev) → architecture §3–4 → prototype-vs-design; rồi đọc `functions-and-features.js` của LAB-1 để lấy man-day. |
| Hỏi lại trước khi làm | AskUserQuestion | 3 câu (tiếng Việt): không có skill chấm SWP chính thức thì xử lý thế nào, mã học viên, tên/độ public của repo. Học viên chọn: tự viết skill, dùng `haiht-1795`, repo `lab5-product-b-backlog`. |
| Break task | Không dùng skill có sẵn. AI viết thẳng `backlog/backlog.json` | Ràng buộc đưa cho AI: (a) mỗi dòng T-xx của constraint-traceability hoặc user story LAB-4 → ≥ 1 issue; ô "Kiểm chứng" thành Done; (b) OQ mang theo chế độ CFG/STUB/BLOCK của sổ OQ; (c) F08 tách epic giờ lái 2024 riêng; (d) feature chỉ có ở mức kiến trúc → issue thô `needs-design`; (e) mọi tính năng LAB-1 phải được ít nhất 1 issue phủ (có script kiểm). |
| Chấm SWP | Skill tự viết [skills/swp-scoring](skills/swp-scoring/SKILL.md) | AI chấm S/C khi viết backlog; skill tính SWP, flag, chọn mẫu, xuất HTML. Thang chấm và +1 pháp lý viết trong SKILL.md để lần sau chấm lại ra cùng kết quả. |
| Quy giờ | Cùng skill | Quy ước cố định `SWP × 4h × k` nằm trong code (estimate.md §2), không để AI ước giờ tự do từng issue. |
| Ghi SWP lên Project | Agent chạy script `gh` | AI viết [github-issues-sync.py](scripts/github-issues-sync.py) (tạo issue, nối sub-issue) và [github-project-sync.py](scripts/github-project-sync.py) (tạo trường, ghi Status/Iteration/SWP/Giờ/Phụ trách/Cấp/Ràng buộc bằng GraphQL theo lô 20 mutation). Script chỉ đọc `backlog-scored.json` sau review, nên SWP trên Project là SWP đã chốt. Script chạy lại được (map khóa → số issue trong `github-map.json`), không tạo trùng. |
| Báo cáo tiến độ | Skill `dataviz` (quy tắc vẽ biểu đồ) + script [burndown-chart-svg.py](scripts/burndown-chart-svg.py) | Nhật ký ngày giả lập viết tay ở `backlog/sprint-1-daily-log.json` (issue/sub-issue xong ngày nào). Script tính SWP/giờ còn lại và vẽ SVG một trục. Bảng trạng thái render từ dữ liệu, không gõ tay. |
| Kiểm kế hoạch | Script [plan-capacity-check.py](scripts/plan-capacity-check.py) | Sau khi học viên hỏi lại "plan có chỗ nào không hợp lý, trạng thái và giờ ước/thực tế đã đồng bộ chưa": tính tải từng người theo sprint so với năng lực (đã chia hệ số thực tế/ước), kiểm phụ thuộc, lập bảng giờ ước/thực tế/còn lại. |
| Tài liệu | Script [render-doc-tables.py](scripts/render-doc-tables.py) | Văn bản viết ở `doc-templates/`. Bảng số liệu và số issue `#n` được script điền vào, tránh lệch giữa tài liệu và Project. |

## 2. Review output của AI

**Người review ở các bước:**
1. **Trước khi làm:** học viên chốt cách xử lý thiếu skill SWP, tên repo, độ public (vì repo/Project public là hành động ra ngoài).
2. **Sau khi skill chọn mẫu:** quyết định chốt SWP cho 26 issue mẫu nằm trong [swp-review.json](backlog/swp-review.json). **Bản này do AI soạn theo vai người review; học viên đọc lại từng dòng đối chiếu spec LAB-4 rồi mới chốt.** Mọi sửa đổi chỉ cần sửa file JSON rồi chạy lại skill + sync.
3. **Trước khi nộp:** học viên mở repo và Project bằng cửa sổ ẩn danh, đọc progress-report.md với vai khách hàng.

**Vấn đề phát hiện trong output của AI và cách xử lý:**

| # | Vấn đề | Ai/cái gì phát hiện | Xử lý |
|---|---|---|---|
| 1 | 13 issue chia sub-issue quá lớn (> 16h) hoặc issue > 24h không tách | Skill (flag SUB-BIG/NEED-SUB) | Chia lại sub-issue, giữ SWP; chạy lại skill sạch flag |
| 2 | Chạy lại skill sau khi sửa thì danh sách mẫu đổi, mất vết "skill chọn → người chốt" | Kiểm báo cáo HTML | Đóng băng mẫu của lần chạy đầu (`samplesFirstRun`) |
| 3 | Skill cộng +1 pháp lý cho cổng công bố (#{I-0809}) dù ngưỡng luật nằm ở issue khác | Review mẫu | Giảm C 4 → 3, SWP 13 → 8 |
| 4 | Skill chấm dỡ đơn G4 (#{I-0604}) như việc nội bộ F06, bỏ sót việc kiểm lại giờ lái | Review mẫu | Tăng S 3 → 4, SWP 8 → 13 |
| 5 | Tính năng FT-04-06 (kiểm khớp vùng nhiệt) không có issue nào phủ | Script kiểm phủ 74 tính năng LAB-1 | Gán vào #{I-0301} |
| 6 | Tổng LAB-5 thấp hơn LAB-1 ≈ 45%; các epic thô thấp 48–73% | Bảng so sánh tự sinh | Không chỉnh số cho khớp. Ghi nguyên nhân (chưa issue hóa, khác cơ sở giờ/ngày) và đưa thành rủi ro R-06 |
| 7 | Văn bản báo cáo ghi sai ngày đường burndown đi ngang, sai số issue "+1 pháp lý" (9 → 8) | Tự đối chiếu văn bản với bảng sinh ra | Sửa văn bản; số trong bảng do script sinh nên không sai |
| 8 | Kế hoạch ban đầu chỉ cân tổng SWP/giờ, không cân theo người: Sprint 1 BE2 152%, FE1 27%; Sprint 2 sơ bộ BE2 193%; panel kiểm giờ (#{I-0808}) xếp trước khi có tuyến (#{I-0701}); không có giờ thực tế | Học viên hỏi lại; script kiểm tải + phụ thuộc | Cân lại người phụ trách Sprint 1, thêm #{I-0205} cho FE1, lập lại Sprint 2–3, thêm trường Giờ thực tế / Giờ còn lại lên Project, thêm rủi ro R-08 |

## 3. Điểm đặc biệt trong cách dùng AI

**Chỗ tin là hiệu quả**
- **Một nguồn dữ liệu, nhiều đầu ra.** `backlog.json` → skill → Project → tài liệu. Khi người review đổi một con số, Project, HTML và cả 4 file Markdown đổi theo. Không có bảng nào gõ tay hai lần.
- **Dùng skill để AI tự bắt lỗi của AI.** Luật độ hạt và luật chọn mẫu viết thành code nên lỗi (#1, #5) được bắt bằng máy, không phụ thuộc vào việc người review có để ý hay không.
- **Ràng buộc đặc thù được mã hóa vào thang chấm** (+1 pháp lý), không phải hệ số nhân ẩn. Nhờ vậy thấy được nó làm tăng effort E08 bao nhiêu, và thấy được chỗ nó bị cộng sai (#3).

**Chỗ chưa tốt, cần cải thiện khi làm thật**
- **Quy ước 4h/SWP chưa có dữ liệu hiệu chỉnh.** Khi làm thật cần lấy giờ thực tế 2–3 sprint đầu để hiệu chỉnh (đội thật, không giả lập).
- **Review mẫu do AI soạn trước** rồi người chốt, nên có nguy cơ người review "đồng ý cho nhanh" (anchoring). Làm thật nên để người chấm độc lập 5–6 mẫu trước khi xem điểm của AI.
- **Epic thô (F07, F10–F13) chỉ là chỗ giữ effort.** AI có xu hướng ước thấp khi spec mỏng. Lẽ ra phải để skill flag "issue thiếu spec mà SWP thấp".
- **Chi phí token:** đọc trọn các technical-spec 30–45 KB của LAB-4 rất tốn; lần sau chỉ đọc mục Requirements/User Stories và bảng truy vết.
- **View của Project** (Board "Board — Sprint 1" chia cột theo Status, lọc Sprint 1 + Cấp = Issue) học viên tạo tay trên giao diện vì GitHub API chưa hỗ trợ tạo view. Trường hệ thống *Parent issue* không Group by được nên script thêm trường single-select `Epic` để nhóm theo epic.
