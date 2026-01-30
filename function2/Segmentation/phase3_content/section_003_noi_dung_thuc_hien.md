# Chương 3: Nội dung thực hiện và kết quả

## 3.1 Môi trường thực tập

### 3.1.1 Giới thiệu đơn vị thực tập

Thực tập được thực hiện tại WENet - đơn vị chuyên về giải pháp IoT và hệ thống kết nối thông minh. WENet có kinh nghiệm triển khai các dự án Edge Computing và Cloud cho doanh nghiệp, campus thông minh và các ứng dụng giám sát công nghiệp.

### 3.1.2 Thiết bị và công cụ sử dụng

**Phần cứng:**
- Edge Gateway: Raspberry Pi 4 / Intel NUC
- Các cảm biến: nhiệt độ, độ ẩm, ánh sáng, chuyển động
- Camera IP cho giám sát

**Phần mềm:**
- Hệ điều hành: Ubuntu Server, Raspberry Pi OS
- Cloud Platform: AWS IoT Core / Azure IoT Hub
- Database: InfluxDB (time-series), PostgreSQL
- Dashboard: Grafana, Node-RED

## 3.2 Quá trình thực hiện

### 3.2.1 Giai đoạn 1: Tìm hiểu và chuẩn bị

Trong giai đoạn đầu, tập trung nghiên cứu:
- Tìm hiểu kiến trúc hệ thống Edge Computing tại WENet
- Nghiên cứu tài liệu về AWS IoT Core và các dịch vụ liên quan
- Làm quen với các thiết bị phần cứng Edge node
- Thiết lập môi trường phát triển cá nhân

**Kết quả giai đoạn 1:**
- Nắm được kiến trúc tổng thể hệ thống
- Thiết lập thành công môi trường development

### 3.2.2 Giai đoạn 2: Cài đặt và cấu hình Edge Node

Tiến hành cài đặt và cấu hình Edge node:

1. **Cài đặt hệ điều hành**: Flash Ubuntu Server lên thiết bị
2. **Cấu hình mạng**: Thiết lập IP tĩnh, kết nối WiFi/Ethernet
3. **Cài đặt phần mềm**: Docker, Python, Node.js
4. **Kết nối cảm biến**: Cấu hình GPIO, I2C cho các cảm biến
5. **Viết script thu thập dữ liệu**: Python script đọc dữ liệu từ sensors

**Code mẫu thu thập dữ liệu:**
```python
import time
import json
from sensors import read_temperature, read_humidity

def collect_data():
    data = {
        "timestamp": time.time(),
        "temperature": read_temperature(),
        "humidity": read_humidity()
    }
    return json.dumps(data)
```

### 3.2.3 Giai đoạn 3: Kết nối Edge với Cloud

Thiết lập kết nối giữa Edge node và AWS IoT Core:

1. **Tạo Thing trong AWS IoT**: Đăng ký thiết bị trên console
2. **Tải Certificate**: Download và cấu hình chứng chỉ X.509
3. **Cài đặt AWS IoT SDK**: Sử dụng Python SDK
4. **Thiết lập MQTT connection**: Kết nối và publish data
5. **Tạo IoT Rules**: Định tuyến data đến các service khác

**Kết quả:**
- Kết nối thành công Edge → Cloud qua MQTT
- Dữ liệu được gửi real-time với độ trễ < 500ms

### 3.2.4 Giai đoạn 4: Xây dựng Dashboard

Phát triển dashboard hiển thị dữ liệu:

- **Backend**: Node.js + Express API
- **Database**: InfluxDB lưu trữ time-series data
- **Frontend**: React dashboard với charts
- **Visualization**: Grafana panels cho monitoring

**Tính năng dashboard:**
- Hiển thị nhiệt độ, độ ẩm real-time
- Biểu đồ lịch sử 24h/7 ngày
- Cảnh báo ngưỡng (alerts)
- Export dữ liệu CSV

## 3.3 Kết quả đạt được

### 3.3.1 Sản phẩm demo

Hoàn thành hệ thống demo với các thành phần:

| Thành phần | Mô tả | Trạng thái |
|------------|-------|------------|
| Edge Node | Raspberry Pi + sensors | ✅ Hoạt động |
| Cloud Backend | AWS IoT + Lambda | ✅ Hoạt động |
| Database | InfluxDB | ✅ Hoạt động |
| Dashboard | Grafana | ✅ Hoạt động |

### 3.3.2 Hiệu năng hệ thống

Kết quả đo đạc hiệu năng:
- **Độ trễ trung bình**: 300-500ms (Edge → Cloud)
- **Uptime**: 99.5% trong thời gian test
- **Data loss rate**: < 0.1%
- **Tần suất gửi data**: 1 sample/giây

### 3.3.3 Kinh nghiệm học được

Qua quá trình thực tập, đã tích lũy được:
- Kỹ năng cài đặt và cấu hình thiết bị Edge
- Hiểu biết về cloud architecture và IoT protocols
- Kinh nghiệm debug hệ thống phân tán
- Kỹ năng làm việc nhóm và báo cáo kỹ thuật
