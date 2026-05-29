import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def __init__(self, broker="127.0.0.1", port=1883, topic="edge/gesture/counts"):
        self.broker = broker
        self.port = port
        self.topic = topic
        # 使用 paho-mqtt v2.0.0+ 要求的 API 版本
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        self.client.on_connect = self._on_connect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"[MQTT] Successfully connected to broker {self.broker}:{self.port}")
        else:
            print(f"[MQTT] Failed to connect, reason code: {reason_code}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"[MQTT] Broker 連線失敗: {e}")

    def publish_counts(self, counts):
        payload = json.dumps(counts)
        self.client.publish(self.topic, payload)
        print(f"[MQTT] Published: {payload}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()