import paho.mqtt.client as mqtt

broker = "broker.emqx.io"
topic = "aiot/nhom6/alerts"

def on_message(client, userdata, msg):
    print(f"\nĐÃ NHẬN ĐƯỢC TỪ KÊNH '{msg.topic}':")
    print(msg.payload.decode("utf-8"))

client = mqtt.Client()
client.on_message = on_message
client.connect(broker, 1883, 60)
client.subscribe(topic)

print("Đang túc trực chờ nhận dữ liệu từ AI...")
client.loop_forever()