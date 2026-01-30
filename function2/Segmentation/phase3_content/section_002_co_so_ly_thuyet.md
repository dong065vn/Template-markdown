# Chương 2: Cơ sở lý thuyết

## 2.1 Tổng quan về Edge Computing

### 2.1.1 Khái niệm Edge Computing

Edge Computing (Điện toán biên) là mô hình điện toán phân tán trong đó việc xử lý dữ liệu được thực hiện gần nguồn dữ liệu nhất, thay vì dựa hoàn toàn vào trung tâm dữ liệu tập trung. Điều này giúp giảm độ trễ, tiết kiệm băng thông và tăng cường khả năng xử lý thời gian thực.

Trong kiến trúc Edge Computing, các thiết bị biên (Edge devices) như gateway, router thông minh, hoặc máy chủ nhỏ đóng vai trò xử lý dữ liệu trước khi gửi lên Cloud. Điều này đặc biệt quan trọng trong các ứng dụng yêu cầu phản hồi nhanh như xe tự lái, giám sát an ninh, hoặc tự động hóa công nghiệp.

### 2.1.2 Kiến trúc hệ thống Edge

Kiến trúc Edge Computing điển hình bao gồm ba tầng chính:

1. **Tầng thiết bị (Device Layer)**: Bao gồm các cảm biến, camera, thiết bị IoT thu thập dữ liệu thô từ môi trường.

2. **Tầng Edge (Edge Layer)**: Các Edge node xử lý dữ liệu sơ bộ, lọc nhiễu, tổng hợp và đưa ra quyết định cục bộ. Đây là nơi xử lý độ trễ thấp diễn ra.

3. **Tầng Cloud (Cloud Layer)**: Lưu trữ dữ liệu dài hạn, phân tích nâng cao, huấn luyện mô hình AI và quản lý tập trung toàn hệ thống.

### 2.1.3 Ưu điểm của Edge Computing

- **Giảm độ trễ**: Xử lý tại chỗ giúp phản hồi trong milliseconds thay vì seconds
- **Tiết kiệm băng thông**: Chỉ gửi dữ liệu đã xử lý lên Cloud
- **Tăng độ tin cậy**: Hoạt động độc lập khi mất kết nối internet
- **Bảo mật tốt hơn**: Dữ liệu nhạy cảm có thể được xử lý cục bộ

## 2.2 Cloud Computing

### 2.2.1 Khái niệm Cloud Computing

Cloud Computing (Điện toán đám mây) là mô hình cung cấp tài nguyên máy tính qua internet theo nhu cầu, bao gồm máy chủ, lưu trữ, cơ sở dữ liệu, mạng và phần mềm. Người dùng không cần đầu tư hạ tầng vật lý mà có thể thuê tài nguyên linh hoạt.

### 2.2.2 Các nền tảng Cloud phổ biến

**Amazon Web Services (AWS)**:
- EC2: Dịch vụ máy chủ ảo
- S3: Lưu trữ đối tượng
- IoT Core: Quản lý thiết bị IoT
- Lambda: Serverless computing

**Microsoft Azure**:
- Virtual Machines: Máy chủ ảo
- Blob Storage: Lưu trữ
- IoT Hub: Quản lý thiết bị IoT
- Functions: Serverless computing

### 2.2.3 Mô hình dịch vụ Cloud

- **IaaS (Infrastructure as a Service)**: Cung cấp hạ tầng (máy chủ, lưu trữ, mạng)
- **PaaS (Platform as a Service)**: Cung cấp nền tảng phát triển ứng dụng
- **SaaS (Software as a Service)**: Cung cấp phần mềm qua internet

## 2.3 Tích hợp Edge và Cloud

### 2.3.1 Kiến trúc Edge-Cloud

Sự kết hợp giữa Edge và Cloud tạo nên kiến trúc lai (Hybrid Architecture) tối ưu:

```
[Sensors/IoT] → [Edge Gateway] → [Cloud Platform] → [Dashboard/App]
      ↓              ↓                  ↓
   Thu thập     Xử lý sơ bộ        Lưu trữ + AI
```

### 2.3.2 Giao thức kết nối

Các giao thức phổ biến trong kết nối Edge-Cloud:
- **MQTT**: Giao thức nhẹ phù hợp IoT
- **HTTP/HTTPS**: Giao thức web tiêu chuẩn
- **WebSocket**: Kết nối hai chiều thời gian thực
- **CoAP**: Giao thức cho thiết bị hạn chế tài nguyên

### 2.3.3 Bảo mật trong hệ thống Edge-Cloud

- **Mã hóa đầu cuối**: TLS/SSL cho dữ liệu truyền tải
- **Xác thực thiết bị**: Chứng chỉ X.509, API keys
- **Quản lý quyền truy cập**: IAM policies, RBAC
- **Giám sát an ninh**: Log monitoring, anomaly detection
