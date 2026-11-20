import paho.mqtt.client as mqtt
import json

broker = "broker.emqx.io" # Server test miễn phí
topic = "aiot/nhom6/alerts"

client = mqtt.Client()
client.connect(broker, 1883, 60)

# Cục dữ liệu mock data chuẩn đã chốt
payload = {
  "event_id": "EVT_001",
  "type": "anomaly",
  "description": "bọt tràn / dị vật",
  "image_path": "/local/images/evt_001.jpg"
}

client.publish(topic, json.dumps(payload))
print("ĐÃ GỬI: Tín hiệu phát hiện dị vật lên mạng!")