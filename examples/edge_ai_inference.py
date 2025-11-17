"""
Edge AI Inference Example
TensorFlow Lite inference on IoT devices
"""

import numpy as np
import time
import json
from datetime import datetime

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    print("⚠️  tflite_runtime not found, using tensorflow instead")
    import tensorflow as tf
    tflite = tf.lite

class EdgeAIInference:
    def __init__(self, model_path="model.tflite"):
        """Initialize TFLite interpreter"""
        print(f"🤖 Loading TFLite model: {model_path}")

        # For demo purposes, we'll create a simple mock interpreter
        # In production, load actual .tflite model
        self.model_loaded = False
        try:
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()

            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.model_loaded = True
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            print("📝 Running in simulation mode")

    def preprocess_sensor_data(self, temperature, humidity, pressure=1013.25):
        """Preprocess sensor data for inference"""
        # Normalize values (example normalization)
        temp_norm = (temperature - 20) / 30  # Normalize around 20°C
        humid_norm = humidity / 100
        pressure_norm = (pressure - 1000) / 50

        return np.array([[temp_norm, humid_norm, pressure_norm]], dtype=np.float32)

    def predict(self, temperature, humidity, pressure=1013.25):
        """Run inference on sensor data"""
        # Preprocess input
        input_data = self.preprocess_sensor_data(temperature, humidity, pressure)

        if self.model_loaded:
            # Run actual inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

            start_time = time.time()
            self.interpreter.invoke()
            inference_time = (time.time() - start_time) * 1000  # ms

            # Get output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            prediction = output[0]
        else:
            # Simulation mode - simple rule-based prediction
            inference_time = np.random.uniform(5, 15)  # Simulate 5-15ms inference

            # Simulate anomaly detection
            is_anomaly = (temperature < 10 or temperature > 35 or
                         humidity < 20 or humidity > 90)
            prediction = np.array([1.0 if is_anomaly else 0.0])

        return {
            'prediction': float(prediction[0]),
            'inference_time_ms': round(inference_time, 2),
            'is_anomaly': prediction[0] > 0.5,
            'confidence': abs(prediction[0] - 0.5) * 2
        }

    def monitor_sensors(self, duration=60, interval=2):
        """Continuously monitor sensors and run inference"""
        print(f"\n📊 Starting edge AI monitoring for {duration} seconds...")
        print("=" * 60)

        start_time = time.time()
        anomaly_count = 0
        total_predictions = 0
        total_inference_time = 0

        while time.time() - start_time < duration:
            # Simulate sensor readings
            temperature = 22 + np.random.normal(0, 5)
            humidity = 65 + np.random.normal(0, 10)
            pressure = 1013.25 + np.random.normal(0, 5)

            # Run inference
            result = self.predict(temperature, humidity, pressure)

            # Update statistics
            total_predictions += 1
            total_inference_time += result['inference_time_ms']
            if result['is_anomaly']:
                anomaly_count += 1

            # Display results
            timestamp = datetime.now().strftime("%H:%M:%S")
            status = "🔴 ANOMALY" if result['is_anomaly'] else "✅ NORMAL"

            print(f"\n[{timestamp}] {status}")
            print(f"  Temperature: {temperature:6.2f}°C")
            print(f"  Humidity:    {humidity:6.2f}%")
            print(f"  Pressure:    {pressure:6.2f} hPa")
            print(f"  Confidence:  {result['confidence']*100:5.1f}%")
            print(f"  Inference:   {result['inference_time_ms']:5.2f}ms")

            time.sleep(interval)

        # Summary statistics
        print("\n" + "=" * 60)
        print("📈 MONITORING SUMMARY")
        print("=" * 60)
        print(f"Total predictions: {total_predictions}")
        print(f"Anomalies detected: {anomaly_count} ({anomaly_count/total_predictions*100:.1f}%)")
        print(f"Average inference time: {total_inference_time/total_predictions:.2f}ms")
        print(f"Throughput: {total_predictions/(time.time()-start_time):.2f} predictions/sec")

    def export_results(self, results, filename="inference_results.json"):
        """Export results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Results exported to {filename}")

def main():
    print("🚀 Edge AI Inference Demo")
    print("=" * 60)

    # Initialize edge AI
    edge_ai = EdgeAIInference()

    # Single prediction example
    print("\n📍 Single Prediction Example:")
    result = edge_ai.predict(temperature=25.5, humidity=68.2)
    print(f"  Prediction: {result['prediction']:.4f}")
    print(f"  Anomaly: {'Yes' if result['is_anomaly'] else 'No'}")
    print(f"  Inference time: {result['inference_time_ms']:.2f}ms")

    # Continuous monitoring
    print("\n" + "=" * 60)
    try:
        edge_ai.monitor_sensors(duration=30, interval=2)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")

    print("\n✅ Edge AI inference demo completed!")

if __name__ == "__main__":
    main()
