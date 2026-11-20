import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# 1. Cấu hình trạm phát MQTT
broker = "broker.emqx.io"
topic = "aiot/nhom6/foam_coverage"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# 2. Xử lý ảnh bằng OpenCV (Tách bọt trắng)
def calculate_foam_coverage(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Không tìm thấy ảnh, đang dùng dữ liệu giả lập...")
        return 82.5 # Mock data nếu không có ảnh

    # Chuyển ảnh sang không gian màu HSV để dễ tách sáng/tối
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Định nghĩa dải màu trắng/xám sáng của bọt
    lower_white = np.array([0, 0, 150])
    upper_white = np.array([180, 50, 255])
    
    # Tạo mặt nạ (mask) chỉ lấy phần bọt
    mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Tính phần trăm
    foam_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    coverage = (foam_pixels / total_pixels) * 100
    return coverage

# Bạn tải 1 tấm ảnh mặt hồ sục khí trên mạng về, lưu là 'be_nuoc.jpg' để cùng thư mục
coverage_percent = calculate_foam_coverage("be_nuoc.jpg")

# 3. Phân loại cảnh báo theo chuẩn (giống bài mẫu nhóm 1)
status = "normal"
if coverage_percent >= 40:
    status = "alarm"
elif coverage_percent >= 25:
    status = "warn"

# 4. Đóng gói JSON và Bắn dữ liệu
payload = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "coverage_percent": round(coverage_percent, 2),
    "status": status,
    "message": "Cảnh báo: Bọt phủ quá mức!" if status == "alarm" else "Bình thường"
}

client.publish(topic, json.dumps(payload))
print(f"\nĐÃ XỬ LÝ ẢNH & GỬI LÊN MẠNG:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")