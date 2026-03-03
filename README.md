# Công cụ Kiểm Tra Dịch Vụ

## Vấn Đề Cần Giải Quyết

Công cụ này được thiết kế để kiểm tra xem dịch vụ có thể cung cấp cho người dùng từ internet hay không. Điều này bao gồm việc xác minh trạng thái dịch vụ, kiểm tra cổng dịch vụ, và đảm bảo rằng các quy tắc tường lửa không ngăn cản kết nối.

## Tại Sao Chọn Tech Stack Này

Chúng tôi chọn Python vì tính linh hoạt và dễ sử dụng của nó trong việc thực hiện các tác vụ hệ thống và mạng. Python có nhiều thư viện hỗ trợ cho việc thực hiện các lệnh hệ thống, kiểm tra kết nối mạng, và ghi log.

## Luồng Hoạt Động Chính

1. **Kiểm Tra Trạng Thái Dịch Vụ**: Sử dụng `systemctl` để kiểm tra trạng thái của dịch vụ.
2. **Kiểm Tra Port Dịch Vụ**: Kiểm tra xem cổng dịch vụ có đang mở và lắng nghe hay không.
3. **Kiểm Tra Tường Lửa Local**: Xác minh rằng tường lửa trên máy chủ không chặn cổng dịch vụ.
4. **Kiểm Tra Tường Lửa Bên Ngoài**: Kiểm tra tường lửa bên ngoài để đảm bảo rằng cổng truy cập từ internet được mở.
5. **Test Kết Nối Tới Internet**: Sử dụng `ping` hoặc `traceroute` để xác minh rằng dịch vụ có thể truy cập từ internet.

## Đầu Vào

- Tên dịch vụ
- Cổng dịch vụ
- Cổng truy cập từ internet vào firewall
- Địa chỉ IP của firewall bên ngoài

## Hướng Dẫn Chạy Công Cụ

Để chạy công cụ kiểm tra dịch vụ, bạn có thể sử dụng lệnh sau trong terminal:

```bash
sudo python3 service_check.py \
  --service nginx \
  --port 80 \
  --protocol tcp \
  --wan-ip 192.168.232.130
```

Trong đó:

- `--service`: Tên dịch vụ bạn muốn kiểm tra (ví dụ: `nginx`).
- `--port`: Cổng dịch vụ (ví dụ: `80`).
- `--protocol`: Loại giao thức (ví dụ: `tcp`).
- `--wan-ip`: Địa chỉ IP của firewall bên ngoài để kiểm tra kết nối.
- Loại giao thức (TCP/UDP/ICMP)

## Đầu Ra

- File log ghi lại các bước kiểm tra và kết quả của từng bước.

## Cấu Trúc Dự Án (Modular Architecture)

Công cụ đã được tái cấu trúc thành các module riêng biệt để dễ debug và bảo trì:

```
tool-service-check/
├── service_check.py      # Main entry point - Điều phối toàn bộ quy trình
├── checks.py             # Lớp ServiceChecker - Chứa tất cả các hàm kiểm tra
├── logger.py             # Lớp Logger - Quản lý logging đến file và console
├── analyzer.py           # Lớp DiagnosticAnalyzer - Phân tích kết quả và đưa ra khuyến nghị
├── utils.py              # Hàm tiện ích - run_cmd để thực thi các lệnh shell
└── README.md             # Tài liệu này
```

### Chi Tiết Các Module

#### **service_check.py** (Main Orchestrator)

- Lớp chính `ServiceDiagnosticTool` để điều phối toàn bộ quy trình
- Phương thức `perform_checks()` - Thực thi tất cả các kiểm tra
- Phương thức `generate_report()` - Tạo báo cáo chi tiết
- Phương thức `run()` - Chạy toàn bộ quy trình

#### **checks.py** (Diagnostic Functions)

- Lớp `ServiceChecker` với các phương thức tĩnh:
  - `check_service()` - Kiểm tra trạng thái dịch vụ
  - `check_port()` - Kiểm tra cổng dịch vụ
  - `check_ufw()` - Kiểm tra tường lửa local
  - `check_ping()` - Kiểm tra kết nối

#### **logger.py** (Logging Management)

- Lớp `Logger` để quản lý ghi log:
  - `log()` - Ghi log đến cả console và file
  - `section()` - Ghi tiêu đề section
  - `raw_output()` - Ghi raw output từ lệnh
  - `result()` - Ghi kết quả

#### **analyzer.py** (Diagnostic Logic)

- Lớp `DiagnosticAnalyzer`:
  - `analyze()` - Phân tích kết quả các kiểm tra
  - `get_status_summary()` - Tạo tóm tắt trạng thái

#### **utils.py** (Utility Functions)

- Hàm `run_cmd()` - Thực thi các lệnh shell

## Ưu Điểm Của Kiến Trúc Modular

1. **Dễ Debug**: Mỗi module có trách nhiệm riêng, dễ tìm lỗi
2. **Dễ Bảo Trì**: Sửa đổi một module không ảnh hưởng đến các module khác
3. **Dễ Mở Rộng**: Có thể thêm các kiểm tra mới mà không phải sửa code cũ
4. **Dễ Test**: Mỗi module có thể được test độc lập
5. **Dễ Đọc**: Code được chia thành các phần nhỏ, dễ hiểu
