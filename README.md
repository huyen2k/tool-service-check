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
