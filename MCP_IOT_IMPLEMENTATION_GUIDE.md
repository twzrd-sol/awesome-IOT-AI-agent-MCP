# MCP IoT Implementation Guide - Practical Examples

## Overview

This guide provides practical implementation examples for integrating Model Context Protocol (MCP) with IoT systems and AI agents.

---

## Architecture Patterns

### Pattern 1: MCP over MQTT Bridge

**Ideal for**: Existing IoT deployments with MQTT infrastructure

```
┌─────────────┐      MQTT        ┌──────────────┐      MCP       ┌──────────┐
│ IoT Devices │ ──────────────► │ Bridge Server│ ─────────────► │ AI Agent │
│  (Sensors)  │                  │  (MCP Server)│                │  Client  │
└─────────────┘                  └──────────────┘                └──────────┘
                                         │
                                    MQTT Publish
                                         ▼
                                  ┌──────────────┐
                                  │   Actuators  │
                                  └──────────────┘
```

#### Components Needed

1. **MQTT Broker**: EMQX or Mosquitto
2. **MCP Bridge Server**: Python or TypeScript
3. **IoT Devices**: Any MQTT-capable sensors/actuators
4. **AI Agent**: MCP client (Claude, custom agent)

#### Example: Python MCP-MQTT Bridge Server

```python
# mcp_mqtt_bridge.py
from fastmcp import FastMCP
import paho.mqtt.client as mqtt
import json
from typing import Dict, Any
import asyncio

mcp = FastMCP("iot-mqtt-bridge")

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SENSOR_TOPIC = "sensors/+"
ACTUATOR_TOPIC = "actuators/{device_id}/cmd"

# Store latest sensor data
sensor_data = {}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(SENSOR_TOPIC)

def on_message(client, userdata, msg):
    """Handle incoming MQTT sensor data"""
    try:
        topic_parts = msg.topic.split('/')
        sensor_id = topic_parts[1] if len(topic_parts) > 1 else "unknown"
        data = json.loads(msg.payload.decode())
        sensor_data[sensor_id] = data
        print(f"Received from {sensor_id}: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# MCP Resources - Expose sensor data
@mcp.resource("sensor://list")
def list_sensors() -> str:
    """List all available sensors"""
    return json.dumps({
        "sensors": list(sensor_data.keys()),
        "count": len(sensor_data)
    })

@mcp.resource("sensor://{sensor_id}/data")
def get_sensor_data(sensor_id: str) -> str:
    """Get latest data from specific sensor"""
    if sensor_id in sensor_data:
        return json.dumps(sensor_data[sensor_id])
    return json.dumps({"error": "Sensor not found"})

# MCP Tools - Control actuators
@mcp.tool()
def control_actuator(device_id: str, command: str, value: Any) -> Dict[str, Any]:
    """
    Send command to IoT actuator via MQTT

    Args:
        device_id: ID of the actuator device
        command: Command to execute (e.g., 'set_state', 'set_value')
        value: Value for the command
    """
    try:
        topic = ACTUATOR_TOPIC.format(device_id=device_id)
        payload = json.dumps({
            "command": command,
            "value": value,
            "timestamp": asyncio.get_event_loop().time()
        })

        mqtt_client.publish(topic, payload)

        return {
            "success": True,
            "device_id": device_id,
            "command": command,
            "value": value
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
def get_all_sensor_readings() -> Dict[str, Any]:
    """Get readings from all connected sensors"""
    return {
        "timestamp": asyncio.get_event_loop().time(),
        "sensors": sensor_data
    }

@mcp.tool()
def analyze_environment(location: str) -> Dict[str, Any]:
    """
    Analyze environmental conditions from multiple sensors

    Args:
        location: Location identifier (e.g., 'room1', 'zone_a')
    """
    # Filter sensors by location
    location_sensors = {
        k: v for k, v in sensor_data.items()
        if location in k.lower()
    }

    if not location_sensors:
        return {"error": f"No sensors found for location: {location}"}

    # Aggregate data
    temps = []
    humidity = []
    co2 = []

    for sensor_id, data in location_sensors.items():
        if "temperature" in data:
            temps.append(data["temperature"])
        if "humidity" in data:
            humidity.append(data["humidity"])
        if "co2" in data:
            co2.append(data["co2"])

    analysis = {
        "location": location,
        "sensor_count": len(location_sensors),
        "conditions": {}
    }

    if temps:
        analysis["conditions"]["temperature"] = {
            "avg": sum(temps) / len(temps),
            "min": min(temps),
            "max": max(temps)
        }

    if humidity:
        analysis["conditions"]["humidity"] = {
            "avg": sum(humidity) / len(humidity),
            "min": min(humidity),
            "max": max(humidity)
        }

    if co2:
        co2_avg = sum(co2) / len(co2)
        analysis["conditions"]["co2"] = {
            "avg": co2_avg,
            "status": "high" if co2_avg > 1000 else "normal"
        }

    return analysis

# MCP Prompts - Common workflows
@mcp.prompt()
def smart_building_control() -> str:
    """Prompt for smart building environmental control"""
    return """You are a smart building AI assistant with access to environmental sensors and HVAC controls.

Available capabilities:
1. Read temperature, humidity, CO2, and occupancy sensors
2. Control HVAC systems, windows, and lighting
3. Analyze environmental conditions
4. Optimize for comfort and energy efficiency

When analyzing conditions:
- Ideal temperature: 20-24°C
- Ideal humidity: 40-60%
- CO2 safe limit: <1000 ppm
- Consider occupancy levels

Your goal is to maintain comfortable, healthy, and energy-efficient conditions."""

@mcp.prompt()
def predictive_maintenance() -> str:
    """Prompt for predictive maintenance analysis"""
    return """You are an industrial IoT maintenance AI with access to equipment sensors.

Analyze sensor data for:
1. Unusual patterns or anomalies
2. Signs of degradation or wear
3. Predictive failure indicators
4. Maintenance recommendations

Consider:
- Historical baselines
- Operating thresholds
- Failure patterns
- Maintenance schedules

Provide actionable recommendations with priority levels."""

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
```

#### Running the Bridge Server

```bash
# Install dependencies
pip install fastmcp paho-mqtt

# Run the server
python mcp_mqtt_bridge.py

# Configure in Claude Desktop (claude_desktop_config.json)
{
  "mcpServers": {
    "iot-mqtt-bridge": {
      "command": "python",
      "args": ["/path/to/mcp_mqtt_bridge.py"]
    }
  }
}
```

---

### Pattern 2: Edge MCP Server for Direct Device Integration

**Ideal for**: High-performance, low-latency requirements

#### Example: TypeScript Edge Server

```typescript
// iot-edge-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Simulated sensor interface (replace with actual hardware interface)
interface SensorReading {
  temperature: number;
  humidity: number;
  timestamp: number;
}

class IoTEdgeServer {
  private server: Server;
  private sensorCache: Map<string, SensorReading>;

  constructor() {
    this.server = new Server(
      {
        name: "iot-edge-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          resources: {},
          tools: {},
          prompts: {},
        },
      }
    );

    this.sensorCache = new Map();
    this.setupHandlers();
    this.startSensorPolling();
  }

  private setupHandlers() {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      const resources = Array.from(this.sensorCache.keys()).map((sensorId) => ({
        uri: `sensor://${sensorId}`,
        name: `Sensor ${sensorId}`,
        description: `Real-time data from sensor ${sensorId}`,
        mimeType: "application/json",
      }));

      return { resources };
    });

    // Read resource data
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;
      const match = uri.match(/^sensor:\/\/(.+)$/);

      if (!match) {
        throw new Error(`Invalid sensor URI: ${uri}`);
      }

      const sensorId = match[1];
      const reading = this.sensorCache.get(sensorId);

      if (!reading) {
        throw new Error(`Sensor not found: ${sensorId}`);
      }

      return {
        contents: [
          {
            uri,
            mimeType: "application/json",
            text: JSON.stringify(reading, null, 2),
          },
        ],
      };
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "read_sensor",
            description: "Read current value from a sensor",
            inputSchema: {
              type: "object",
              properties: {
                sensor_id: {
                  type: "string",
                  description: "ID of the sensor to read",
                },
              },
              required: ["sensor_id"],
            },
          },
          {
            name: "control_device",
            description: "Send control command to an actuator",
            inputSchema: {
              type: "object",
              properties: {
                device_id: {
                  type: "string",
                  description: "ID of the device to control",
                },
                action: {
                  type: "string",
                  description: "Action to perform",
                  enum: ["on", "off", "set_value"],
                },
                value: {
                  type: "number",
                  description: "Value for set_value action",
                },
              },
              required: ["device_id", "action"],
            },
          },
          {
            name: "get_environmental_status",
            description: "Get aggregated environmental status",
            inputSchema: {
              type: "object",
              properties: {
                zone: {
                  type: "string",
                  description: "Zone identifier (optional)",
                },
              },
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case "read_sensor":
          return this.handleReadSensor(args.sensor_id as string);

        case "control_device":
          return this.handleControlDevice(
            args.device_id as string,
            args.action as string,
            args.value as number | undefined
          );

        case "get_environmental_status":
          return this.handleGetEnvironmentalStatus(args.zone as string | undefined);

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  private async handleReadSensor(sensorId: string) {
    const reading = this.sensorCache.get(sensorId);

    if (!reading) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Sensor ${sensorId} not found` }),
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(reading, null, 2),
        },
      ],
    };
  }

  private async handleControlDevice(
    deviceId: string,
    action: string,
    value?: number
  ) {
    // Simulate device control (replace with actual hardware interface)
    console.log(`Controlling device ${deviceId}: ${action}`, value);

    // In production, this would interface with actual hardware
    const result = {
      device_id: deviceId,
      action,
      value,
      status: "success",
      timestamp: Date.now(),
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleGetEnvironmentalStatus(zone?: string) {
    const sensors = Array.from(this.sensorCache.entries());
    const filteredSensors = zone
      ? sensors.filter(([id]) => id.includes(zone))
      : sensors;

    if (filteredSensors.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: "No sensors found" }),
          },
        ],
      };
    }

    const temperatures = filteredSensors.map(([, reading]) => reading.temperature);
    const humidities = filteredSensors.map(([, reading]) => reading.humidity);

    const status = {
      zone: zone || "all",
      sensor_count: filteredSensors.length,
      temperature: {
        avg: temperatures.reduce((a, b) => a + b, 0) / temperatures.length,
        min: Math.min(...temperatures),
        max: Math.max(...temperatures),
      },
      humidity: {
        avg: humidities.reduce((a, b) => a + b, 0) / humidities.length,
        min: Math.min(...humidities),
        max: Math.max(...humidities),
      },
      timestamp: Date.now(),
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(status, null, 2),
        },
      ],
    };
  }

  private startSensorPolling() {
    // Simulate sensor readings (replace with actual sensor interface)
    setInterval(() => {
      // Simulate 3 sensors
      for (let i = 1; i <= 3; i++) {
        this.sensorCache.set(`sensor_${i}`, {
          temperature: 20 + Math.random() * 5,
          humidity: 40 + Math.random() * 20,
          timestamp: Date.now(),
        });
      }
    }, 1000); // Update every second
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("IoT Edge MCP Server running on stdio");
  }
}

// Run the server
const server = new IoTEdgeServer();
server.run().catch(console.error);
```

#### Build and Run

```bash
# Install dependencies
npm install @modelcontextprotocol/sdk

# Build TypeScript
npx tsc iot-edge-server.ts

# Run
node iot-edge-server.js

# Or configure in Claude Desktop
{
  "mcpServers": {
    "iot-edge": {
      "command": "node",
      "args": ["/path/to/iot-edge-server.js"]
    }
  }
}
```

---

### Pattern 3: Cloud-Deployed Remote MCP Server

**Ideal for**: Scalable, multi-tenant IoT platforms

#### Example: Containerized Remote Server

```python
# remote_iot_server.py
from fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
from typing import Dict, List, Optional
import os

# Initialize FastMCP with SSE support
mcp = FastMCP("cloud-iot-platform")

# Simulated IoT device registry
class DeviceRegistry:
    def __init__(self):
        self.devices: Dict[str, Dict] = {}

    def register_device(self, device_id: str, device_type: str, metadata: Dict):
        self.devices[device_id] = {
            "type": device_type,
            "metadata": metadata,
            "last_seen": asyncio.get_event_loop().time(),
            "status": "online"
        }

    def get_device(self, device_id: str) -> Optional[Dict]:
        return self.devices.get(device_id)

    def list_devices(self, device_type: Optional[str] = None) -> List[Dict]:
        devices = list(self.devices.items())
        if device_type:
            devices = [(id, dev) for id, dev in devices if dev["type"] == device_type]
        return [{"id": id, **dev} for id, dev in devices]

registry = DeviceRegistry()

# Initialize with some mock devices
registry.register_device("temp_001", "temperature_sensor", {"location": "room1", "unit": "celsius"})
registry.register_device("humid_001", "humidity_sensor", {"location": "room1", "unit": "percent"})
registry.register_device("hvac_001", "hvac_controller", {"location": "room1", "capacity": "5kW"})

# MCP Tools
@mcp.tool()
def list_devices(device_type: Optional[str] = None) -> List[Dict]:
    """
    List all registered IoT devices

    Args:
        device_type: Optional filter by device type
    """
    return registry.list_devices(device_type)

@mcp.tool()
def get_device_info(device_id: str) -> Dict:
    """
    Get detailed information about a specific device

    Args:
        device_id: Unique device identifier
    """
    device = registry.get_device(device_id)
    if not device:
        return {"error": f"Device {device_id} not found"}
    return {"id": device_id, **device}

@mcp.tool()
def read_device_data(device_id: str) -> Dict:
    """
    Read current data from an IoT device

    Args:
        device_id: Device to read from
    """
    device = registry.get_device(device_id)
    if not device:
        return {"error": f"Device {device_id} not found"}

    # Simulate reading data based on device type
    if device["type"] == "temperature_sensor":
        return {
            "device_id": device_id,
            "temperature": 22.5,
            "unit": "celsius",
            "timestamp": asyncio.get_event_loop().time()
        }
    elif device["type"] == "humidity_sensor":
        return {
            "device_id": device_id,
            "humidity": 45.0,
            "unit": "percent",
            "timestamp": asyncio.get_event_loop().time()
        }

    return {"error": "Device type not supported for reading"}

@mcp.tool()
def control_device(device_id: str, command: str, parameters: Optional[Dict] = None) -> Dict:
    """
    Send control command to an IoT device

    Args:
        device_id: Device to control
        command: Command to execute
        parameters: Optional command parameters
    """
    device = registry.get_device(device_id)
    if not device:
        return {"error": f"Device {device_id} not found"}

    # Simulate device control
    result = {
        "device_id": device_id,
        "command": command,
        "parameters": parameters or {},
        "status": "executed",
        "timestamp": asyncio.get_event_loop().time()
    }

    return result

@mcp.tool()
def analyze_zone_environment(zone: str) -> Dict:
    """
    Analyze environmental conditions for a zone

    Args:
        zone: Zone identifier (e.g., 'room1', 'floor2')
    """
    # Get all devices in the zone
    zone_devices = [
        (id, dev) for id, dev in registry.devices.items()
        if dev["metadata"].get("location") == zone
    ]

    if not zone_devices:
        return {"error": f"No devices found in zone {zone}"}

    # Aggregate environmental data
    temp_sensors = [id for id, dev in zone_devices if dev["type"] == "temperature_sensor"]
    humid_sensors = [id for id, dev in zone_devices if dev["type"] == "humidity_sensor"]

    analysis = {
        "zone": zone,
        "device_count": len(zone_devices),
        "temperature": 22.5 if temp_sensors else None,  # Simulated
        "humidity": 45.0 if humid_sensors else None,    # Simulated
        "air_quality": "good",
        "recommendations": []
    }

    # Add recommendations based on conditions
    if analysis["temperature"] and analysis["temperature"] > 24:
        analysis["recommendations"].append("Temperature high - consider increasing cooling")
    if analysis["humidity"] and analysis["humidity"] > 60:
        analysis["recommendations"].append("Humidity high - increase ventilation")

    return analysis

# MCP Resources
@mcp.resource("devices://list")
def devices_list() -> str:
    """List of all registered devices"""
    devices = registry.list_devices()
    return json.dumps(devices, indent=2)

@mcp.resource("devices://{device_id}")
def device_detail(device_id: str) -> str:
    """Detailed information about a specific device"""
    device = registry.get_device(device_id)
    if not device:
        return json.dumps({"error": "Device not found"})
    return json.dumps({"id": device_id, **device}, indent=2)

# MCP Prompts
@mcp.prompt()
def facility_manager_assistant() -> str:
    """AI assistant for facility management"""
    return """You are an AI facility manager with access to building IoT systems.

Your capabilities:
- Monitor temperature, humidity, and air quality sensors
- Control HVAC, lighting, and ventilation systems
- Analyze environmental conditions by zone
- Provide energy optimization recommendations
- Detect anomalies and suggest maintenance

Best practices:
- Always check current conditions before making changes
- Consider occupancy and time of day
- Prioritize occupant comfort and safety
- Optimize for energy efficiency when possible
- Log all control actions for audit trail"""

@mcp.prompt()
def energy_optimization() -> str:
    """Energy optimization analysis prompt"""
    return """Analyze current building systems for energy optimization opportunities.

Review:
1. Current HVAC settings and usage patterns
2. Occupancy levels and schedules
3. Temperature and humidity readings
4. Equipment runtime and efficiency

Provide recommendations for:
- Schedule adjustments
- Setpoint optimization
- Equipment runtime reduction
- Predictive scheduling based on occupancy

Estimate potential energy savings for each recommendation."""

if __name__ == "__main__":
    # For remote deployment, use HTTP+SSE transport
    import uvicorn
    app = mcp.get_asgi_app()  # FastMCP provides ASGI app for remote deployment
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY remote_iot_server.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run server
CMD ["python", "remote_iot_server.py"]
```

#### requirements.txt

```txt
fastmcp>=2.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
```

#### Deploy to Google Cloud Run

```bash
# Build and deploy
gcloud run deploy iot-mcp-server \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ENV=production"

# Get the service URL
gcloud run services describe iot-mcp-server \
  --region us-central1 \
  --format="value(status.url)"
```

#### Connect Client to Remote Server

```python
# client_example.py
from mcp_use import MCPClient
import asyncio

async def main():
    # Connect to remote MCP server
    async with MCPClient("https://your-cloud-run-url.run.app") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", tools)

        # Call a tool
        result = await client.call_tool(
            "analyze_zone_environment",
            {"zone": "room1"}
        )
        print("Zone analysis:", result)

        # Read a resource
        devices = await client.read_resource("devices://list")
        print("Devices:", devices)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Hardware Integration Examples

### Example 1: Raspberry Pi with DHT22 Sensor

```python
# raspberry_pi_mcp_server.py
from fastmcp import FastMCP
import Adafruit_DHT
import time
from typing import Dict

mcp = FastMCP("raspberry-pi-sensors")

# DHT22 sensor configuration
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin 4

@mcp.tool()
def read_temperature_humidity() -> Dict:
    """Read temperature and humidity from DHT22 sensor"""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "unit_temp": "celsius",
            "unit_humid": "percent",
            "timestamp": time.time()
        }
    else:
        return {
            "error": "Failed to read sensor",
            "timestamp": time.time()
        }

@mcp.resource("sensor://dht22/current")
def current_reading() -> str:
    """Current sensor reading as resource"""
    import json
    data = read_temperature_humidity()
    return json.dumps(data)

if __name__ == "__main__":
    mcp.run()
```

### Example 2: ESP32 MQTT to MCP Bridge

```python
# esp32_mqtt_bridge.py
"""
Bridge for ESP32 devices publishing sensor data via MQTT
Exposes data through MCP for AI agent consumption
"""

from fastmcp import FastMCP
import paho.mqtt.client as mqtt
import json
from collections import defaultdict
import time

mcp = FastMCP("esp32-bridge")

# Store sensor data from ESP32 devices
esp32_data = defaultdict(dict)

# MQTT Configuration
MQTT_BROKER = "192.168.1.100"  # Your MQTT broker IP
MQTT_PORT = 1883
ESP32_TOPIC = "esp32/+/sensors"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT: {rc}")
    client.subscribe(ESP32_TOPIC)

def on_message(client, userdata, msg):
    """Handle MQTT messages from ESP32 devices"""
    try:
        # Topic format: esp32/{device_id}/sensors
        device_id = msg.topic.split('/')[1]
        data = json.loads(msg.payload.decode())

        # Store latest data
        esp32_data[device_id] = {
            **data,
            "last_update": time.time()
        }

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Setup MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()

@mcp.tool()
def list_esp32_devices() -> dict:
    """List all ESP32 devices that have reported data"""
    devices = []
    current_time = time.time()

    for device_id, data in esp32_data.items():
        last_seen = current_time - data.get("last_update", 0)
        devices.append({
            "device_id": device_id,
            "status": "online" if last_seen < 60 else "offline",
            "last_seen_seconds": int(last_seen)
        })

    return {"devices": devices, "count": len(devices)}

@mcp.tool()
def get_esp32_data(device_id: str) -> dict:
    """Get latest sensor data from specific ESP32 device"""
    if device_id not in esp32_data:
        return {"error": f"Device {device_id} not found"}

    return esp32_data[device_id]

@mcp.tool()
def get_all_temperature_readings() -> dict:
    """Get temperature readings from all ESP32 devices"""
    temps = {}
    for device_id, data in esp32_data.items():
        if "temperature" in data:
            temps[device_id] = {
                "temperature": data["temperature"],
                "unit": data.get("temp_unit", "celsius"),
                "last_update": data["last_update"]
            }

    if not temps:
        return {"error": "No temperature sensors found"}

    # Calculate average
    avg_temp = sum(t["temperature"] for t in temps.values()) / len(temps)

    return {
        "sensors": temps,
        "average_temperature": round(avg_temp, 2),
        "count": len(temps)
    }

@mcp.resource("esp32://devices")
def esp32_devices_resource() -> str:
    """Resource listing all ESP32 devices"""
    return json.dumps(list_esp32_devices(), indent=2)

@mcp.resource("esp32://{device_id}/latest")
def esp32_device_data(device_id: str) -> str:
    """Resource for specific ESP32 device data"""
    return json.dumps(get_esp32_data(device_id), indent=2)

if __name__ == "__main__":
    print("ESP32 MQTT-MCP Bridge starting...")
    mcp.run()
```

### Example 3: Arduino with Serial Communication

```python
# arduino_serial_mcp.py
"""
MCP server for Arduino devices connected via serial/USB
"""

from fastmcp import FastMCP
import serial
import json
import time
from threading import Thread, Lock

mcp = FastMCP("arduino-serial")

# Serial configuration
SERIAL_PORT = "/dev/ttyUSB0"  # Adjust for your system
BAUD_RATE = 9600

# Thread-safe data storage
data_lock = Lock()
arduino_data = {}

class ArduinoReader(Thread):
    def __init__(self, port, baud_rate):
        super().__init__(daemon=True)
        self.serial = serial.Serial(port, baud_rate, timeout=1)
        self.running = True

    def run(self):
        """Continuously read from Arduino"""
        while self.running:
            try:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8').strip()
                    data = json.loads(line)

                    with data_lock:
                        arduino_data.update({
                            **data,
                            "timestamp": time.time()
                        })
            except Exception as e:
                print(f"Serial read error: {e}")
                time.sleep(1)

    def write_command(self, command: str):
        """Send command to Arduino"""
        self.serial.write(f"{command}\n".encode())

# Start Arduino reader thread
arduino_reader = ArduinoReader(SERIAL_PORT, BAUD_RATE)
arduino_reader.start()

@mcp.tool()
def read_arduino_sensors() -> dict:
    """Read all sensor values from Arduino"""
    with data_lock:
        return dict(arduino_data)

@mcp.tool()
def send_arduino_command(command: str, value: int = 0) -> dict:
    """
    Send command to Arduino

    Args:
        command: Command to send (e.g., 'LED_ON', 'SET_SERVO')
        value: Optional value parameter
    """
    try:
        cmd_str = f"{command}:{value}"
        arduino_reader.write_command(cmd_str)
        return {
            "success": True,
            "command": command,
            "value": value,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.resource("arduino://sensors/all")
def all_sensors() -> str:
    """All Arduino sensor readings"""
    return json.dumps(read_arduino_sensors(), indent=2)

if __name__ == "__main__":
    print(f"Arduino MCP server starting on {SERIAL_PORT}")
    mcp.run()
```

---

## Testing and Debugging

### Test MCP Server Locally

```python
# test_mcp_server.py
"""
Test script for MCP servers
"""

import asyncio
from mcp_use import MCPClient

async def test_server():
    # For local stdio server
    async with MCPClient(
        command="python",
        args=["your_mcp_server.py"]
    ) as client:
        # Test listing tools
        print("=== Available Tools ===")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")

        # Test listing resources
        print("\n=== Available Resources ===")
        resources = await client.list_resources()
        for resource in resources:
            print(f"- {resource['uri']}: {resource['name']}")

        # Test calling a tool
        print("\n=== Testing Tool Call ===")
        result = await client.call_tool(
            "read_sensor",
            {"sensor_id": "sensor_1"}
        )
        print(f"Result: {result}")

        # Test reading a resource
        print("\n=== Testing Resource Read ===")
        resource_data = await client.read_resource("sensor://list")
        print(f"Resource: {resource_data}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

### MCP Inspector for Debugging

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test your server
npx @modelcontextprotocol/inspector python your_mcp_server.py

# For TypeScript servers
npx @modelcontextprotocol/inspector node your_server.js
```

### Logging Configuration

```python
# Add comprehensive logging to your MCP server

import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

mcp = FastMCP("iot-server")

@mcp.tool()
def monitored_tool(param: str) -> dict:
    """Example tool with logging"""
    logger.info(f"Tool called with param: {param}")

    try:
        result = {"status": "success", "param": param}
        logger.info(f"Tool completed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
```

---

## Performance Optimization

### Request Batching

```python
from fastmcp import FastMCP
from typing import List, Dict
import asyncio

mcp = FastMCP("optimized-iot")

@mcp.tool()
async def batch_read_sensors(sensor_ids: List[str]) -> Dict:
    """
    Read multiple sensors in parallel for better performance

    Args:
        sensor_ids: List of sensor IDs to read
    """
    async def read_one(sensor_id: str):
        # Simulate sensor read
        await asyncio.sleep(0.1)  # Async I/O
        return {sensor_id: {"value": 42, "unit": "celsius"}}

    # Read all sensors in parallel
    results = await asyncio.gather(*[read_one(sid) for sid in sensor_ids])

    # Combine results
    combined = {}
    for result in results:
        combined.update(result)

    return combined
```

### Caching for Frequently Accessed Data

```python
from fastmcp import FastMCP
from functools import lru_cache
import time

mcp = FastMCP("cached-iot")

# Cache device metadata (doesn't change often)
@lru_cache(maxsize=1000)
def get_device_metadata(device_id: str) -> dict:
    """Cached device metadata lookup"""
    # Expensive database lookup here
    return {
        "device_id": device_id,
        "type": "sensor",
        "location": "room1"
    }

# Time-based cache for sensor data
class SensorCache:
    def __init__(self, ttl=5):
        self.cache = {}
        self.ttl = ttl  # Time to live in seconds

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

sensor_cache = SensorCache(ttl=5)

@mcp.tool()
def read_sensor_cached(sensor_id: str) -> dict:
    """Read sensor with 5-second cache"""
    # Check cache first
    cached = sensor_cache.get(sensor_id)
    if cached:
        return {**cached, "from_cache": True}

    # Read fresh data
    data = {"value": 42, "unit": "celsius", "timestamp": time.time()}
    sensor_cache.set(sensor_id, data)

    return {**data, "from_cache": False}
```

---

## Security Implementation Examples

### Authentication with OAuth 2.0

```python
# secure_mcp_server.py
from fastmcp import FastMCP
from fastapi import HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Optional

mcp = FastMCP("secure-iot-server")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = "your-secret-key"  # Use environment variable in production
JWT_ALGORITHM = "HS256"

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

# Apply authentication to tools
@mcp.tool()
def read_secured_sensor(
    sensor_id: str,
    user: dict = Depends(verify_token)
) -> dict:
    """Read sensor with authentication required"""
    # Check user permissions
    if "sensors:read" not in user.get("permissions", []):
        return {"error": "Permission denied"}

    # Read sensor
    return {
        "sensor_id": sensor_id,
        "value": 42,
        "accessed_by": user["username"]
    }
```

### Input Validation

```python
from fastmcp import FastMCP
from pydantic import BaseModel, validator, Field
from typing import Literal

mcp = FastMCP("validated-iot")

class DeviceCommand(BaseModel):
    """Validated device command model"""
    device_id: str = Field(..., regex=r'^[a-z0-9_]+$', max_length=50)
    action: Literal["on", "off", "reset", "configure"]
    value: Optional[int] = Field(None, ge=0, le=100)

    @validator('device_id')
    def device_id_exists(cls, v):
        # Check if device exists
        if not device_exists(v):  # Your lookup function
            raise ValueError(f"Device {v} not found")
        return v

@mcp.tool()
def validated_control_device(
    device_id: str,
    action: str,
    value: Optional[int] = None
) -> dict:
    """Control device with strict input validation"""
    try:
        # Validate input
        command = DeviceCommand(
            device_id=device_id,
            action=action,
            value=value
        )

        # Execute command
        return {
            "success": True,
            "device_id": command.device_id,
            "action": command.action,
            "value": command.value
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

---

## Conclusion

This implementation guide provides practical, production-ready examples for integrating MCP with IoT systems. Key takeaways:

1. **Choose the Right Pattern**: MQTT bridge for existing infrastructure, edge servers for low latency, cloud deployment for scalability
2. **Security First**: Always implement authentication, input validation, and encryption
3. **Optimize Performance**: Use caching, batching, and async operations
4. **Test Thoroughly**: Use MCP Inspector and write comprehensive tests
5. **Monitor Everything**: Implement logging, metrics, and alerting

These examples can be adapted and extended for your specific IoT use cases and hardware platforms.

---

*Implementation Guide Version: 1.0*
*Last Updated: 2025-11-17*
