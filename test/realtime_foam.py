import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# 1. Cấu hình MQTT
broker = "broker.emqx.io"
topic = "aiot/nhom6/foam_coverage"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) # Đã fix cảnh báo
client.connect(broker, 1883, 60)

# 2. Mở Camera hoặc Video
# Số 0: Mở Webcam mặc định của laptop
# Nếu có file video, đổi số 0 thành tên file (vd: "video_be_nuoc.mp4")
cap = cv2.VideoCapture("http://192.168.2.28:4747/video")

print("Đang mở Camera... Đưa một vật màu trắng (như tờ giấy) ra trước cam để test bọt nhé!")
last_send_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không đọc được Camera/Video.")
        break

    # Lật ảnh camera cho thuận mắt (như gương)
    frame = cv2.flip(frame, 1)

    # 3. Xử lý ảnh (Tách màu trắng)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 150])
    upper_white = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    
    foam_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    coverage_percent = (foam_pixels / total_pixels) * 100

    # 4. Phân loại cảnh báo
    status = "normal"
    if coverage_percent >= 40:
        status = "alarm"
    elif coverage_percent >= 25:
        status = "warn"

    # 5. Hiển thị màn hình Camera trực tiếp
    cv2.imshow("Cam Thuc Te", frame)
    cv2.imshow("Vung Bot (Mask)", mask) # Hiện vùng màu trắng nó bóc được

    # 6. Bắn dữ liệu (Cách 2 giây bắn 1 lần để web không bị nghẽn)
    current_time = time.time()
    if current_time - last_send_time >= 2:
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "coverage_percent": round(coverage_percent, 2),
            "status": status
        }
        client.publish(topic, json.dumps(payload))
        print(f"[{payload['timestamp']}] Mật độ: {payload['coverage_percent']}% -> {status}")
        last_send_time = current_time

    # Bấm phím 'q' trên bàn phím để thoát chương trình
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Dọn dẹp khi tắt
cap.release()
cv2.destroyAllWindows()