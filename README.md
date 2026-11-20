[readme_h_th_ng_aiot_gi_m_s_t_b_t_n_c_th_i.md](https://github.com/user-attachments/files/35125274/readme_h_th_ng_aiot_gi_m_s_t_b_t_n_c_th_i.md)
# 🌊 Hệ thống AIoT Giám sát & Cảnh báo Bọt Nước Thải (Nhóm 6)

Hệ thống giám sát bề mặt bể xử lý nước thải theo thời gian thực (Real-time), ứng dụng Thị giác máy tính (Computer Vision) để phát hiện mật độ bọt nổi, phân loại mức độ cảnh báo và truyền dữ liệu trực tiếp qua giao thức MQTT lên Dashboard hiển thị.

---

## 🏗️ Kiến trúc hệ thống

```text
[Camera / Video / IP Cam] 
         │
         ▼
[Edge AI - Python (OpenCV / YOLOv8)]  ──► Xử lý ảnh, tính % độ phủ bọt & phân loại cảnh báo
         │
         ▼ (MQTT - JSON Payload)
[MQTT Broker: broker.emqx.io:1883]    ──► Topic: aiot/nhom6/foam_coverage
         │
         ▼
[Dashboard UI (Node-RED / Custom Web)] ──► Hiển thị đồng hồ đo, biểu đồ & cảnh báo Real-time
```

---

## ⚙️ Tính năng hiện có (MVP)

- **Phân tích ảnh & Video Real-time:** Hỗ trợ chạy kiểm thử trên ảnh tĩnh (`solo_foam_detector.py`) và luồng video trực tiếp (`realtime_foam.py`).
- **Tích hợp đa nguồn Camera:** Tương thích với Webcam laptop, Camera rời (USB), Camera điện thoại qua mạng LAN (IP Webcam/DroidCam) và Camera giám sát công nghiệp (RTSP).
- **Phân loại cảnh báo tự động (3 mức độ):**
  - 🟢 **Normal (`normal`):** Độ phủ bọt `< 25%`
  - 🟡 **Warning (`warn`):** Độ phủ bọt từ `25%` đến `< 40%`
  - 🔴 **Alarm (`alarm`):** Độ phủ bọt `>= 40%`
- **Truyền thông IoT độ trễ thấp:** Đẩy dữ liệu định kỳ mỗi 2 giây qua giao thức MQTT.
- **Dashboard trực quan:** Hiển thị thông số theo thời gian thực trên Node-RED Dashboard với dải màu cảnh báo tự động.

---

## 🛠️ Yêu cầu môi trường & Cài đặt

### 1. Cài đặt thư viện Python (Module AI & IoT)
Yêu cầu cài đặt Python 3.8 trở lên. Chạy lệnh sau trong Terminal/PowerShell:

```bash
pip install opencv-python numpy paho-mqtt
```

### 2. Cài đặt Node-RED (Module Dashboard)
Yêu cầu cài đặt [Node.js](https://nodejs.org/). Sau đó cài đặt Node-RED toàn cục:

```bash
npm install -g --unsafe-perm node-red
```
*Lưu ý:* Trong giao diện Node-RED (`http://localhost:1880`), vào **Menu $\rightarrow$ Manage palette $\rightarrow$ Install**, tìm và cài đặt gói `node-red-dashboard`.

---

## 🚀 Hướng dẫn chạy hệ thống

Hệ thống cần chạy song song **2 cửa sổ Terminal** (1 cho Web Dashboard, 1 cho AI Camera):

### Bước 1: Khởi động Node-RED Dashboard
Mở Terminal thứ nhất và chạy:
```bash
node-red
```
Sau khi thấy thông báo `Server now running`, mở trình duyệt và truy cập:
- Trang cấu hình luồng: `http://localhost:1880`
- Trang giao diện đồng hồ giám sát: `http://localhost:1880/ui`

### Bước 2: Khởi động Module AI Camera
Mở Terminal thứ hai, di chuyển vào thư mục dự án và chạy:
```bash
# Chạy chế độ Real-time (Camera/Video)
python realtime_foam.py

# Hoặc chạy kiểm thử 1 ảnh tĩnh (cần có file be_nuoc.jpg cùng thư mục)
python solo_foam_detector.py
```
*Để tắt chương trình AI:* Click vào cửa sổ hiển thị Camera và nhấn phím **`q`** (hoặc nhấn `Ctrl + C` trong Terminal).

---

## 📷 Cấu hình đổi nguồn Camera

Trong file `realtime_foam.py`, thay đổi tham số tại dòng `cap = cv2.VideoCapture(...)` tùy theo thiết bị sử dụng:

| Thiết bị | Cách cấu hình code | Ghi chú |
| :--- | :--- | :--- |
| **Webcam Laptop** | `cv2.VideoCapture(0)` | Mặc định |
| **Webcam rời (USB)** | `cv2.VideoCapture(1)` | Có thể thử `1` hoặc `2` |
| **Điện thoại Android (LAN)** | `cv2.VideoCapture("http://<IP_DIEN_THOAI>:8080/video")` | Dùng app **IP Webcam** (chung Wi-Fi) |
| **Điện thoại iOS/Android** | `cv2.VideoCapture("http://<IP_DIEN_THOAI>:4747/video")` | Dùng app **DroidCam** (chung Wi-Fi) |
| **Camera giám sát (CCTV)** | `cv2.VideoCapture("rtsp://user:pass@<IP>:554/stream1")` | Chuẩn giao thức RTSP |
| **File Video mẫu** | `cv2.VideoCapture("video_be_nuoc.mp4")` | Đặt file video cùng thư mục |

*(Mẹo: Khi dùng camera sau của điện thoại hoặc CCTV, nên comment dòng `frame = cv2.flip(frame, 1)` để hình ảnh không bị lật ngược).*

---

## 🔗 Tài liệu tích hợp cho thành viên nhóm

Hệ thống được thiết kế theo kiến trúc tách rời (Decoupled) thông qua MQTT để các thành viên dễ dàng phát triển song song và ghép nối:

### 1. Thông số kết nối MQTT (Dành cho Team Web/UI)
- **Broker:** `broker.emqx.io`
- **Port (TCP):** `1883`
- **Port (WebSockets cho Web Frontend):** `8083` (hoặc `8084` cho WSS)
- **Topic:** `aiot/nhom6/foam_coverage`

### 2. Cấu trúc dữ liệu JSON (Payload)
Dữ liệu bắn lên MQTT hiện tại có định dạng:
```json
{
  "timestamp": "2026-11-06 23:12:34",
  "coverage_percent": 44.89,
  "status": "alarm",
  "message": "Cảnh báo: Bọt phủ quá mức!"
}
```

### 3. Lộ trình nâng cấp (Roadmap)
- [x] Dựng hoàn chỉnh luồng MVP: Camera $\rightarrow$ OpenCV $\rightarrow$ MQTT $\rightarrow$ Node-RED Dashboard.
- [ ] **Team AI:** Thay thế thuật toán tách màu OpenCV bằng mô hình **YOLOv8-seg** (huấn luyện qua Roboflow) để nhận diện đa đối tượng: *Bọt khí, Bùn, Váng dầu, Dị vật (rác), Khói/Lửa*.
- [ ] **Team Web:** Xây dựng Custom Web Dashboard lắng nghe topic MQTT trên để hiển thị biểu đồ lịch sử, luồng camera và log cảnh báo sự cố.
