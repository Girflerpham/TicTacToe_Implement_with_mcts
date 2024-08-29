# Monte Carlo Tree Search (MCTS) - Thuật toán và Ứng dụng

## I. Giới thiệu về Monte Carlo Tree Search

### a. Tổng quan

Monte Carlo Tree Search (MCTS) là một phương pháp tìm kiếm dựa trên mẫu ngẫu nhiên, sử dụng các lượt giả lập để ước lượng tỷ lệ thắng thua của một trạng thái bàn cờ nhằm tìm ra nước đi tốt nhất. MCTS nổi bật nhờ khả năng cân bằng giữa khám phá và khai thác, đồng thời không phụ thuộc vào tri thức chuyên biệt của trò chơi, tức là không yêu cầu hàm lượng giá trạng thái. Điều này làm cho MCTS trở nên lý tưởng cho nhiều loại trò chơi có thông tin trạng thái rõ ràng và không có yếu tố may rủi, đặc biệt là những trò chơi khó xây dựng hàm lượng giá tốt như cờ Vây.

### b. Cấu trúc và cơ chế của cây tìm kiếm Monte Carlo

MCTS hoạt động qua một quy trình lặp đi lặp lại bốn bước trong một khoảng thời gian hữu hạn:

1. **Lựa chọn (Selection)**: Bắt đầu từ nút gốc (trạng thái hiện tại), thuật toán duyệt qua các nút cho đến khi tìm thấy nút lá. Công thức UCB (Upper Confidence Bound) được sử dụng để đánh giá và lựa chọn nút tiếp theo. Với C = 1, công thức này giúp tìm ra sự cân bằng giữa việc thăm dò các nút mới và khai thác các nút đã biết.

2. **Mở rộng (Expansion)**: Khi đạt đến một nút lá, thuật toán sẽ mở rộng cây bằng cách thêm nút con mới. Việc mở rộng chỉ xảy ra nếu ván cờ chưa kết thúc tại nút lá.

3. **Mô phỏng (Simulation)**: Một loạt các nước đi ngẫu nhiên được thực hiện từ nút mới thêm vào cho đến khi đạt được kết quả. Giai đoạn này giúp ước lượng giá trị của nút mới.

4. **Lan truyền ngược (Backpropagation)**: Sau khi mô phỏng hoàn tất, kết quả được lan truyền ngược từ nút mới lên đến nút gốc, cập nhật số liệu cho các nút trên đường đi.

Cây trò chơi ngày càng mở rộng và sâu hơn sau mỗi lần lặp lại của MCTS. Những nước đi có triển vọng nhất sẽ được chọn trong quá trình lựa chọn, và qua thời gian, việc lấy mẫu sẽ ngày càng chính xác hơn.

### c. Ưu và nhược điểm của MCTS

#### Ưu điểm:

1. **Dễ triển khai**: MCTS là một thuật toán tương đối đơn giản để cài đặt.
2. **Heuristic mạnh mẽ**: MCTS không yêu cầu tri thức chuyên biệt ngoài luật chơi và điều kiện kết thúc, giúp nó tự học và cải thiện qua các lần chơi giả lập.
3. **Tính khả chuyển**: MCTS có thể lưu trữ trạng thái trung gian để tái sử dụng trong các lượt chơi tương lai.
4. **Mở rộng không đối xứng**: Cây tìm kiếm của MCTS có thể mở rộng một cách không đối xứng dựa trên tình huống cụ thể.

#### Nhược điểm:

1. **Yêu cầu bộ nhớ lớn**: Khi cây tìm kiếm phát triển nhanh chóng, nhu cầu bộ nhớ tăng cao.
2. **Vấn đề độ tin cậy**: Do số lượng lớn các tổ hợp, MCTS có thể không truy cập đủ các nút để hiểu rõ kết quả, hoặc cần quá nhiều thời gian để tìm kiếm.
3. **Tốc độ**: MCTS cần nhiều lần lặp để xác định đường đi tốt nhất, do đó tốc độ tìm kiếm có thể trở thành một vấn đề.

### d. Độ phức tạp thời gian và không gian

- **Độ phức tạp thời gian**: O(mkI/C)
- **Độ phức tạp không gian**: O(mk)

Trong đó:
- **m** là số nút con.
- **k** là số mô phỏng cho mỗi nút con.

---

## II. Demo Ứng Dụng TicTacToe

[Link Demo Ứng Dụng TicTacToe](#)

---

## III. Tài liệu tham khảo

- [Monte Carlo Tree Search - Stanford](https://stanford.edu/~rezab/classes/cme323/S15/projects/montecarlo_search_tree_report.pdf)
- [Monte Carlo Tree Search trên GeeksforGeeks](https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/)
- [Nghiên cứu về MCTS tại CTU](https://sj.ctu.edu.vn/ql/docgia/download/baibao-31323/12-NGUYEN%20QUOC%20HUY(17-24).pdf)
- [Giới thiệu MCTS bởi Matthew Deakos](http://matthewdeakos.me/2018/03/10/monte-carlo-tree-search/)

---

README này cung cấp một cái nhìn toàn diện về thuật toán MCTS, từ khái niệm cơ bản đến các ứng dụng thực tế, và cả những ưu nhược điểm cụ thể của nó.
