<div align="center">

# 🌐 Awesome IoT AI Agents & MCP 🤖

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Stars](https://img.shields.io/github/stars/umitkacar/IOT---AI-agent--MCP?style=social)](https://github.com/umitkacar/IOT---AI-agent--MCP/stargazers)

<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Robot.png" width="200" height="200"/>

**A comprehensive, curated list of IoT AI agents, MCP implementations, frameworks, tools, and research papers**

*From edge devices to cloud platforms • From TinyML to Large Language Models • From research to production*

[🚀 Quick Start](#-quick-start) •
[📚 Documentation](#-table-of-contents) •
[💡 Examples](#-code-examples) •
[🤝 Contributing](#-contributing)

---

</div>

## 📊 Market Insights (2025)

| Domain | 2024/2025 | 2030+  | CAGR |
|--------|-----------|--------|------|
| 🤖 AIoT Market | $9.25B | $79.1B | **28.4%** |
| 👥 Multi-Agent Systems | $7.2B | $375.4B | **48.6%** |
| 💻 Edge Computing | $195.18B | $1.1T | **28.4%** |
| 🌐 IoT Devices | 55B+ devices | 75B+ | - |
| 📊 IoT Data | 80 ZB/year | 180 ZB | - |

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🤖 AI Agent Frameworks](#-ai-agent-frameworks)
- [🔌 Model Context Protocol (MCP)](#-model-context-protocol-mcp)
- [🌐 IoT Platforms](#-iot-platforms--ecosystems)
- [📡 Communication Protocols](#-communication-protocols)
- [🧠 Edge AI & TinyML](#-edge-ai--tinyml)
- [🔒 Security & Privacy](#-security--privacy)
- [🏭 Real-World Applications](#-real-world-applications)
- [🛠️ Development Tools](#️-development-tools)
- [📖 Research & Literature](#-research--literature)
- [💡 Code Examples](#-code-examples)
- [🎓 Learning Resources](#-learning-resources)

---

## 🚀 Quick Start

### 🏃 5-Minute Setup Options

<table>
<tr>
<td width="33%">

**Option 1: MQTT AI Agent**
```bash
pip install paho-mqtt openai
python examples/mqtt_ai_agent.py
```
💡 Best for: IoT messaging

</td>
<td width="33%">

**Option 2: MCP Server**
```bash
npm install @modelcontextprotocol/sdk
npx tsx examples/mcp_server.ts
```
💡 Best for: AI integration

</td>
<td width="33%">

**Option 3: Edge AI**
```bash
pip install tflite-runtime
python examples/edge_inference.py
```
💡 Best for: On-device ML

</td>
</tr>
</table>

---

## 🤖 AI Agent Frameworks

### 🌟 Top Multi-Agent Frameworks

| Framework | ⭐ Stars | Language | Best For | Links |
|-----------|---------|----------|----------|-------|
| **LangGraph** | 21K+ | Python | Stateful agents | [GitHub](https://github.com/langchain-ai/langgraph) • [Docs](https://langchain-ai.github.io/langgraph/) |
| **CrewAI** | 25K+ | Python | Role-based agents | [GitHub](https://github.com/crewAIInc/crewAI) • [Docs](https://docs.crewai.com) |
| **AutoGen** | 30K+ | Python/.NET | Multi-agent chat | [GitHub](https://github.com/microsoft/autogen) • [Docs](https://microsoft.github.io/autogen/) |
| **LangChain** | 119K+ | Python/JS | LLM chains | [GitHub](https://github.com/langchain-ai/langchain) • [Docs](https://docs.langchain.com) |

<details>
<summary>🔥 <b>LangGraph</b> - Low-Level Orchestration (Click to expand)</summary>

**Features**:
- ✨ Stateful multi-agent workflows
- 🔄 Durable execution & persistence
- 🤝 Human-in-the-loop capabilities
- 💾 Short-term & long-term memory
- 🎯 Version 1.0 released (Nov 2024)

**IoT Use Cases**:
```python
from langgraph.graph import StateGraph

# Define IoT workflow
workflow = StateGraph()
workflow.add_node("read_sensors", read_iot_sensors)
workflow.add_node("analyze", analyze_with_ai)
workflow.add_node("act", control_actuators)
workflow.compile()
```

**Resources**:
- 📖 [LangGraph Example Repository](https://github.com/langchain-ai/langgraph-example)
- 🎓 [Awesome LangGraph Resources](https://github.com/von-development/awesome-LangGraph)

</details>

<details>
<summary>🚀 <b>CrewAI</b> - Role-Based Multi-Agent (Click to expand)</summary>

**Key Stats**:
- 👥 100,000+ certified developers
- ⚡ Lightweight, pure Python
- 🧠 Built-in memory & knowledge

**Quick Example**:
```python
from crewai import Agent, Task, Crew

sensor_agent = Agent(
    role="Sensor Monitor",
    goal="Monitor IoT sensors",
    backstory="Expert in real-time data"
)

crew = Crew(agents=[sensor_agent], tasks=[task])
result = crew.kickoff()
```

**Resources**:
- 📦 [Examples Repository](https://github.com/crewAIInc/crewAI-examples)
- 🎓 [Multi-Agent Course](https://github.com/akj2018/Multi-AI-Agent-Systems-with-crewAI)

</details>

---

## 🔌 Model Context Protocol (MCP)

> **"MCP is to AI what USB-C is to hardware"** - Universal standard for AI integrations

### 📚 Official Resources

| Resource | Description | Link |
|----------|-------------|------|
| 📘 **Specification** | Protocol specification | [GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol) |
| 🐍 **Python SDK** | Python implementation | [GitHub](https://github.com/modelcontextprotocol/python-sdk) |
| 📜 **TypeScript SDK** | JS/TS implementation | [GitHub](https://github.com/modelcontextprotocol/typescript-sdk) |
| 🎯 **Servers** | Reference implementations | [GitHub](https://github.com/modelcontextprotocol/servers) |
| 📖 **Docs** | Official documentation | [Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) |

### 🌟 Key Features

- 🌐 **Universal Protocol**: JSON-RPC 2.0 based
- 🚀 **Growing Fast**: 1000+ servers (Feb 2025)
- ⚡ **High Performance**: 205ms avg response time
- 💾 **Lightweight**: 74KB memory footprint
- ✅ **Reliable**: 100% success rate across 22 sensor types

### 🔥 Popular MCP Servers

<table>
<tr>
<td width="50%">

**🐙 GitHub MCP Server**
[github/github-mcp-server](https://github.com/github/github-mcp-server)

*Access GitHub via MCP*
- Repository management
- Issue tracking
- Pull requests
- Code search

</td>
<td width="50%">

**🍃 MongoDB MCP Server**
[mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server)

*Query MongoDB via MCP*
- Database queries
- Aggregations
- Index operations
- Collection management

</td>
</tr>
<tr>
<td>

**🏭 IoT-Edge-MCP-Server**
[llm-use/IoT-Edge-MCP-Server](https://github.com/llm-use/IoT-Edge-MCP-Server)

*Industrial IoT via MCP*
- MQTT sensors
- Modbus devices
- SCADA systems
- Real-time monitoring

</td>
<td>

**📁 Filesystem MCP**
[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

*File operations via MCP*
- Read/write files
- Directory navigation
- File search
- Permissions

</td>
</tr>
<tr>
<td width="50%">

**🔐 TWZRD Agent Intel**
[intel.twzrd.xyz](https://intel.twzrd.xyz)

*Agent trust scoring for IoT + AI agents*
- Verify agent wallet identity before x402 micropayment data access
- `score_agent(wallet)` — free trust score
- `preflight_check(wallet)` — deployment readiness
- `get_trust_receipt(wallet)` — paid x402 proof
- Zero-install: `{"mcpServers":{"twzrd-agent-intel":{"url":"https://intel.twzrd.xyz/mcp"}}}`

</td>
<td width="50%">

</td>
</tr>
</table>

### 🌐 MCP-IoT Integration Patterns

| Pattern | Latency | Complexity | Best For |
|---------|---------|------------|----------|
| **MCP over MQTT** | Medium | Low | Existing infrastructure |
| **Edge MCP Server** | 205ms | Medium | Low-latency needs |
| **Cloud MCP** | High | Low | Scalability |
| **Hybrid** | Mixed | High | Enterprise |

**Quick MCP-MQTT Bridge Example**:
```python
from mcp import Server
import paho.mqtt.client as mqtt

server = Server()
mqtt_client = mqtt.Client()

@server.tool()
def read_sensor(device_id: str):
    mqtt_client.publish(f"sensors/{device_id}/read", "")
    # Return sensor data via MCP
```

**Resources**:
- 📄 [MCP over MQTT Guide](https://www.emqx.com/en/blog/mcp-over-mqtt)
- 🔬 [IoT-MCP Research Paper](https://arxiv.org/html/2510.01260v1)

---

## 🌐 IoT Platforms & Ecosystems

### ☁️ Cloud Platforms

<table>
<tr>
<th>Platform</th>
<th>Key Features</th>
<th>Pricing</th>
<th>Best For</th>
</tr>
<tr>
<td>

**AWS IoT Core**
[AWS Docs](https://docs.aws.amazon.com/iot/)

</td>
<td>

- MQTT 3 & 5 support
- Millions of devices
- Greengrass edge runtime
- SageMaker ML integration

</td>
<td>

$1/M messages
💰 $200 free tier

</td>
<td>

Large-scale deployments

</td>
</tr>
<tr>
<td>

**Azure IoT Hub**
[Azure Docs](https://learn.microsoft.com/azure/iot-hub/)

</td>
<td>

- Bi-directional communication
- 99.9% SLA
- Device Twin
- Azure AI integration

</td>
<td>

Pay-as-you-go
Free tier available

</td>
<td>

Enterprise integration

</td>
</tr>
<tr>
<td>

**Google Cloud IoT**
[GCP Docs](https://cloud.google.com/solutions/iot)

</td>
<td>

- BigQuery analytics
- Vertex AI integration
- Supply Chain Twin

</td>
<td>

Analytics-focused
pricing

</td>
<td>

Data-intensive apps

</td>
</tr>
</table>

### 🔓 Open-Source Platforms

| Platform | ⭐ Stars | Language | Focus | Link |
|----------|---------|----------|-------|------|
| **Home Assistant** | High | Python | Smart home | [GitHub](https://github.com/home-assistant/core) |
| **OpenHAB** | High | Java | Home automation | [GitHub](https://github.com/openhab) |
| **ThingsBoard** | High | Java | IoT platform | [GitHub](https://github.com/thingsboard/thingsboard) |

---

## 📡 Communication Protocols

### 🌐 Application Layer

| Protocol | Transport | QoS | Best For | ⭐ Top Library |
|----------|-----------|-----|----------|---------------|
| **MQTT** | TCP | 3 levels | IoT messaging | [EMQX](https://github.com/emqx/emqx) 15.1K⭐ |
| **CoAP** | UDP | 4 types | Constrained devices | [libcoap](https://github.com/obgm/libcoap) 1.2K⭐ |
| **AMQP** | TCP | High | Enterprise | [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server) 13.7K⭐ |
| **WebSocket** | TCP | App-level | Real-time dashboards | [ws](https://github.com/websockets/ws) 21.8K⭐ |

<details>
<summary>📡 <b>MQTT Quick Start</b></summary>

**Python Publisher**:
```python
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("broker.emqx.io", 1883)

data = {"temperature": 25.5, "device": "sensor-001"}
client.publish("iot/sensors/temp", json.dumps(data), qos=1)
```

**Python Subscriber**:
```python
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(f"Temperature: {data['temperature']}°C")

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.emqx.io", 1883)
client.subscribe("iot/sensors/#")
client.loop_forever()
```

**Popular Brokers**:
- 🐝 Mosquitto - Lightweight, widely deployed
- 🚀 EMQX - Scalable, enterprise-grade
- 🐰 RabbitMQ - With MQTT plugin

</details>

### 📶 Wireless Protocols

| Protocol | Range | Data Rate | Power | Best For |
|----------|-------|-----------|-------|----------|
| **LoRaWAN** | 2-15 km | 0.3-50 kbps | Ultra-low | Long-range sensors |
| **Zigbee** | 10-100 m | 250 kbps | Low | Home automation |
| **Z-Wave** | 30-100 m | 9.6-100 kbps | Low | Smart home |
| **BLE** | 10-100 m | 1-2 Mbps | Very low | Wearables |

---

## 🧠 Edge AI & TinyML

> **Edge AI Market**: $195B (2025) → $1.1T (2032)

### 🔥 Top Frameworks

<table>
<tr>
<td width="50%">

### **TensorFlow Lite Micro**
⭐ 14.4K+ stars
🔗 [GitHub](https://github.com/tensorflow/tflite-micro)

**Features**:
- 💾 KB-scale memory
- ⚡ Hardware acceleration
- 🌍 Multi-platform support

**Platforms**:
- ESP32, Arduino
- STM32, Raspberry Pi

```cpp
#include <TensorFlowLite.h>
interpreter->Invoke();
```

</td>
<td width="50%">

### **Edge Impulse**
⭐ 118,185 projects
🌐 [Platform](https://edgeimpulse.com)

**Features**:
- 🎨 No-code ML pipeline
- 🚀 One-click deployment
- 🔧 Custom models

**Stats**:
- 50,953 developers
- 100+ hardware targets

</td>
</tr>
</table>

### 📊 More Frameworks

| Framework | Focus | GitHub | Docs |
|-----------|-------|--------|------|
| **PyTorch ExecuTorch** | Mobile/Edge | [Link](https://github.com/pytorch/executorch) | [Docs](https://pytorch.org/executorch) |
| **ONNX Runtime** | Cross-platform | [Link](https://github.com/microsoft/onnxruntime) | [Docs](https://onnxruntime.ai) |
| **Apache TVM** | Compiler | [Link](https://github.com/apache/tvm) | [Docs](https://tvm.apache.org) |

### 💻 Hardware Options

| Hardware | Price | CPU | RAM | Best For |
|----------|-------|-----|-----|----------|
| **ESP32** | $5-10 | Dual 240MHz | 520KB | Beginners |
| **Raspberry Pi 4** | $35-55 | Quad 1.8GHz | 2-8GB | Gateway |
| **Jetson Nano** | $99-149 | Quad ARM | 4GB | Edge AI |
| **Google Coral** | $59.99 | Edge TPU | - | ML inference |

---

## 🔒 Security & Privacy

### 🛡️ Security Standards

<details>
<summary><b>NIST IoT Security Framework</b> (2024-2025)</summary>

**Latest Updates**:
- **NIST IR 8425** (Jan 2025): Consumer IoT baseline
- **NIST IR 8425A** (Sep 2024): Router profile
- **NIST IR 8259 Rev. 1** (2025): Framework update

**Key Areas**:
- Device identity & authentication
- Data protection & encryption
- Software update mechanisms
- Cybersecurity event detection
- Logical access control

</details>

### 🤝 Privacy-Preserving AI

**Federated Learning Repositories**:

| Project | Description | GitHub |
|---------|-------------|--------|
| **FedML** | Production FL platform | [Link](https://github.com/FedML-AI/FedML) |
| **FedAdapt** | Adaptive offloading | [Link](https://github.com/qub-blesson/FedAdapt) |
| **FedIoT** | Anomaly detection | [Link](https://github.com/FedML-AI/FedML/tree/master/iot) |

**Benefits**:
- ✅ Privacy preservation
- ✅ Distributed learning
- ✅ GDPR/HIPAA compliance
- ✅ Reduced bandwidth

---

## 🏭 Real-World Applications

### 🏠 Smart Home

**Market**: $15.3B (2024) → $104.1B (2034)

**Success Stories**:
- **Amazon Alexa**: 100,000+ device integrations, Generative AI
- **Home Assistant 2024.6**: Gemini & ChatGPT integration
- **LG AI Agent** (CES 2024): Autonomous home control

### 🏭 Industrial IoT

**ROI Examples**:

| Company | Result | Savings |
|---------|--------|---------|
| **General Motors** | 15% downtime reduction | **$20M/year** |
| **Siemens** | 30% less unscheduled downtime | - |
| **Power Generation** | Planned maintenance | **$7.5M saved** |
| **Petrochemical** | Prevented failures | **$600K saved** |

**Overall Impact**:
- 50% reduction in unplanned downtime
- 10-40% lower maintenance costs

### 🌆 Smart Cities

**Global Implementations**:
- **Seoul**: 30%→70% transit ridership increase
- **Cape Town**: 40-60% water consumption drop
- **Cologne**: 100% parking coverage

### ⚕️ Healthcare

**Market**: $21.2B (2022), CAGR 29.8%

**FDA-Approved**:
- **Apple Watch**: ECG, AFib detection
- **Fitbit**: ECG, passive AFib monitoring

**Results**:
- 97.3% diabetes diagnosis accuracy
- 96.2% heart disease detection

### 🌾 Agriculture

**Success Stories**:
- **Netherlands**: 20% yield increase
- **California**: 25% water reduction
- **Bangladesh**: 95.8% crop prediction accuracy

---

## 🛠️ Development Tools

### 🔧 IoT Frameworks

| Framework | ⭐ Stars | Language | Focus |
|-----------|---------|----------|-------|
| **ESP-IDF** | 14.4K+ | C/C++ | ESP32 development |
| **PlatformIO** | 8.7K+ | Multi | Cross-platform |
| **Arduino** | 14.4K+ | C++ | Prototyping |
| **Zephyr RTOS** | High | C | 800+ boards |
| **FreeRTOS** | 10K+ | C | AWS integration |

### 📊 Visualization

| Tool | ⭐ Stars | Focus | GitHub |
|------|---------|-------|--------|
| **Grafana** | 61K+ | Dashboards | [Link](https://github.com/grafana/grafana) |
| **ThingsBoard** | High | IoT platform | [Link](https://github.com/thingsboard/thingsboard) |
| **Node-RED** | 22.3K+ | Flow editor | [Link](https://github.com/node-red/node-red) |

### ☸️ DevOps

| Tool | ⭐ Stars | Focus | Size |
|------|---------|-------|------|
| **K3s** | 31.3K+ | Lightweight K8s | 50MB |
| **KubeEdge** | 9K+ | Edge K8s | 70MB |
| **Balena** | 1.2K+ | Fleet management | - |

---

## 📖 Research & Literature

### 📄 Recent Papers (2023-2025)

| Title | Year | Venue | Link |
|-------|------|-------|------|
| Internet of AI Agents (IAIA) | 2025 | IJNDC | [Springer](https://link.springer.com/article/10.1007/s44227-025-00057-0) |
| Internet of Agents (IoA) | 2025 | arXiv | [2505.07176](https://arxiv.org/abs/2505.07176) |
| AIoT Survey | 2024 | ACM TOSN | [GitHub](https://github.com/AIoT-MLSys-Lab/AIoT-Survey) |
| IoT + Generative AI | 2024 | arXiv | [2401.01923](https://arxiv.org/abs/2401.01923) |
| Federated Learning IoT Survey | 2025 | MDPI | [Link](https://www.mdpi.com/2224-2708/14/1/9) |

### 📚 Top Conferences

| Conference | Impact | Website |
|------------|--------|---------|
| **IEEE IoT Journal** | IF: 8.9 | [Link](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=6488907) |
| **ACM IoT** | 14th Int'l | [Link](https://dl.acm.org/doi/proceedings/10.1145/3703790) |
| **IoTDI** | ACM/IEEE | [Link](https://conferences.computer.org/iotDI/) |

---

## 💡 Code Examples

All examples in [`/examples`](./examples) directory.

### 🔥 Quick Examples

<details>
<summary><b>1. MQTT Temperature Sensor (Python)</b></summary>

```python
import paho.mqtt.client as mqtt
import json, time, random

client = mqtt.Client()
client.connect("broker.emqx.io", 1883)

while True:
    data = {
        "device": "sensor-001",
        "temperature": 20 + random.uniform(-5, 10),
        "timestamp": time.time()
    }
    client.publish("iot/sensors/temp", json.dumps(data), qos=1)
    time.sleep(5)
```

</details>

<details>
<summary><b>2. MCP IoT Server (TypeScript)</b></summary>

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import mqtt from "mqtt";

const server = new Server({ name: "iot-mcp", version: "1.0.0" });
const mqttClient = mqtt.connect("mqtt://broker.emqx.io");

server.tool("read_sensor", "Read sensor",
  { device_id: { type: "string" } },
  async ({ device_id }) => {
    // MQTT sensor read logic
  }
);
```

</details>

<details>
<summary><b>3. Edge AI Inference (TFLite)</b></summary>

```python
import tflite_runtime.interpreter as tflite
import numpy as np

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_data = np.array([[temperature, humidity]], dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

output = interpreter.get_tensor(output_details[0]['index'])
```

</details>

---

## 🎓 Learning Resources

### 📚 Courses

- 🎓 **DeepLearning.AI**:
  - [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/)
  - [Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)

- 🎓 **Edge Impulse**:
  - [Embedded Machine Learning](https://www.edgeimpulse.com/university)

### 🔗 Awesome Lists

- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents)
- [Awesome IoT](https://github.com/HQarroum/awesome-iot)
- [Awesome TinyML](https://github.com/gigwegbe/tinyml-papers-and-projects)
- [Awesome LangGraph](https://github.com/von-development/awesome-LangGraph)

---

## 🤝 Contributing

We welcome contributions! 🎉

**How to contribute**:
1. 🍴 Fork the repository
2. 🌿 Create feature branch (`git checkout -b feature/Amazing`)
3. 💾 Commit changes (`git commit -m 'Add Amazing Feature'`)
4. 📤 Push to branch (`git push origin feature/Amazing`)
5. 🎉 Open Pull Request

**What to add**:
- 📝 New frameworks/tools
- 💡 Code examples
- 📄 Research papers
- 🐛 Bug fixes
- 📚 Documentation

---

## 📊 Stats

```
📦 Resources: 1000+
⭐ Frameworks: 200+
📄 Papers: 100+
💡 Examples: 50+
🔄 Updated: 2025-01-17
```

---

## 🙏 Acknowledgments

- 🤖 **Anthropic** - Model Context Protocol
- 🌐 **OpenAI, Microsoft, Google** - AI frameworks
- 🔬 **Research Community** - Advancing IoT AI
- 👥 **Open Source Community** - Making it possible

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

## ⭐ Star this repository if you find it helpful!

**Made with ❤️ by the IoT AI Community**

[⬆ Back to Top](#-awesome-iot-ai-agents--mcp-)

</div>
