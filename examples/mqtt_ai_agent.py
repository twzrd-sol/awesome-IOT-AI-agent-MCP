"""
MQTT AI Agent Example
Real-time IoT sensor monitoring with AI-powered analysis
"""

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

class IoTSensorAgent:
    def __init__(self, broker="broker.emqx.io", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"✅ Connected to MQTT Broker: {self.broker}")
            client.subscribe("iot/sensors/#", qos=1)
            print("📡 Subscribed to iot/sensors/#")
        else:
            print(f"❌ Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """Process incoming sensor data with AI analysis"""
        try:
            data = json.loads(msg.payload.decode())
            print(f"\n📊 Received data from {msg.topic}")
            print(f"   Device: {data.get('device_id')}")
            print(f"   Temperature: {data.get('temperature')}°C")
            print(f"   Humidity: {data.get('humidity')}%")

            # AI-powered anomaly detection
            self.analyze_sensor_data(data)

        except Exception as e:
            print(f"❌ Error processing message: {e}")

    def analyze_sensor_data(self, data):
        """Simple AI-based anomaly detection"""
        temp = data.get('temperature', 0)
        humidity = data.get('humidity', 0)

        # Threshold-based analysis (can be replaced with ML model)
        if temp > 30:
            print(f"🔥 WARNING: High temperature detected! ({temp}°C)")
        elif temp < 10:
            print(f"❄️  WARNING: Low temperature detected! ({temp}°C)")

        if humidity > 80:
            print(f"💧 WARNING: High humidity detected! ({humidity}%)")
        elif humidity < 30:
            print(f"🏜️  WARNING: Low humidity detected! ({humidity}%)")

    def publish_sensor_data(self, device_id="sensor-001"):
        """Simulate sensor data publishing"""
        while True:
            data = {
                "device_id": device_id,
                "temperature": round(20 + random.uniform(-10, 15), 2),
                "humidity": round(60 + random.uniform(-20, 20), 2),
                "timestamp": datetime.now().isoformat()
            }

            topic = f"iot/sensors/temperature"
            self.client.publish(topic, json.dumps(data), qos=1)
            print(f"📤 Published: {data['temperature']}°C, {data['humidity']}%")
            time.sleep(5)

    def start(self):
        """Start the MQTT agent"""
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        try:
            self.publish_sensor_data()
        except KeyboardInterrupt:
            print("\n🛑 Stopping MQTT agent...")
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    print("🤖 Starting IoT Sensor AI Agent...")
    agent = IoTSensorAgent()
    agent.start()
