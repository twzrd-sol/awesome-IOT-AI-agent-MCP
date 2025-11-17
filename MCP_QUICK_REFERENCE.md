# MCP Quick Reference Guide - IoT & AI Agents

## What is MCP?

Model Context Protocol (MCP) is an **open standard** by Anthropic that standardizes how AI applications connect to data sources, tools, and systems. Think of it as "USB-C for AI."

**Key Benefits:**
- Solves M × N integration problem → M + N
- Standardized communication via JSON-RPC 2.0
- Three core primitives: Resources, Tools, Prompts
- Multiple transport options: stdio, HTTP+SSE, MQTT bridge

---

## Essential Links

### Official Resources
- **Documentation**: https://modelcontextprotocol.io/
- **Specification**: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
- **GitHub**: https://github.com/modelcontextprotocol
- **Claude Docs**: https://docs.anthropic.com/en/docs/agents-and-tools/mcp

### Key Repositories
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Reference Servers**: https://github.com/modelcontextprotocol/servers
- **Awesome Servers**: https://github.com/punkpeye/awesome-mcp-servers
- **GitHub MCP**: https://github.com/github/github-mcp-server
- **Microsoft MCP**: https://github.com/microsoft/mcp

### IoT-Specific
- **IoT-MCP Paper**: https://arxiv.org/html/2510.01260v1
- **MCP over MQTT**: https://www.emqx.com/en/blog/mcp-over-mqtt
- **ThingsPanel**: https://github.com/ThingsPanel/thingspanel-mcp

---

## Quick Start

### Install TypeScript SDK
```bash
npm install @modelcontextprotocol/sdk
```

### Install Python SDK
```bash
pip install mcp
```

### Use FastMCP (Python Alternative)
```bash
pip install fastmcp
```

### Run Reference Server (TypeScript)
```bash
npx @modelcontextprotocol/server-<name>
```

---

## Core Concepts

### The Three Primitives

**1. Resources (Application-controlled)**
- Data sources AI can access
- Like REST API GET endpoints
- Read-only, no side effects
- Examples: files, database records, API responses

**2. Tools (Model-controlled)**
- Executable functions
- Can modify state
- Enable AI to take actions
- Examples: create_ticket, send_email, query_database

**3. Prompts (User-controlled)**
- Reusable templates
- Standardize common workflows
- Encode expert knowledge
- Examples: code_review, bug_analysis, summarize_data

### Transport Options

**stdio (Standard Input/Output)**
- Best for: Local processes
- Pros: Simple, low overhead
- Cons: Local only
- Use case: Desktop apps, CLI tools

**HTTP + SSE (Streamable HTTP)**
- Best for: Remote servers
- Pros: Cloud-compatible, scalable
- Cons: More complex
- Use case: Web services, cloud deployments

**MQTT Bridge (IoT-specific)**
- Best for: IoT devices
- Pros: Reuses MQTT infrastructure
- Cons: Requires bridge server
- Use case: Sensor networks, embedded systems

---

## IoT Implementation Patterns

### Pattern 1: MCP over MQTT
```
IoT Device (MQTT) → MQTT Broker → MCP Server → AI Agent
                                        ↓
                                  Commands back
```

**Benefits:**
- No device firmware changes
- Reuse existing MQTT infrastructure
- Protocol translation at edge
- Scalable for thousands of devices

**Implementation:**
1. MQTT broker (EMQX, Mosquitto)
2. MCP server subscribes to device topics
3. Translates MQTT messages to MCP resources/tools
4. AI agent uses standard MCP client
5. Commands flow back via MQTT

### Pattern 2: Edge MCP Server
```
IoT Devices → Edge MCP Server → Local AI Agent
                    ↓
            Cloud MCP Client (optional)
```

**Benefits:**
- Low latency (205ms avg in research)
- Offline operation
- 74KB memory footprint
- Local processing

**Use Cases:**
- Smart buildings
- Industrial automation
- Real-time control systems
- Privacy-sensitive applications

### Pattern 3: Hybrid Cloud-Edge
```
Edge Devices → Edge MCP Server → AI Agent → Cloud MCP Servers
```

**Benefits:**
- Local + cloud capabilities
- Distributed processing
- Cost optimization
- Flexibility

---

## Security Checklist for IoT

### Authentication & Authorization
- [ ] Implement OAuth 2.0
- [ ] Use TLS 1.3 for all connections
- [ ] NO session-based auth in MCP servers
- [ ] Use non-deterministic session IDs
- [ ] Bind sessions to user information
- [ ] Validate all tokens explicitly

### Input/Output Security
- [ ] Schema validation for all inputs
- [ ] Allow-list expected values
- [ ] Reject unexpected/malformed data
- [ ] Sanitize outputs before sending
- [ ] Implement size limits
- [ ] Filter malicious content

### IoT-Specific Threats
- [ ] Prevent prompt injection via telemetry
- [ ] Implement tool access controls (RBAC)
- [ ] Secure device credentials storage
- [ ] Network segmentation
- [ ] Rate limiting and throttling
- [ ] Audit logging for all actions

### Ongoing Security
- [ ] Regular security updates
- [ ] Dependency vulnerability scanning
- [ ] Monitor security bulletins
- [ ] Incident response plan
- [ ] Security testing in CI/CD
- [ ] Compliance audits

---

## Popular MCP Servers

### Development
- **Git**: Repository operations
- **GitHub**: Issues, PRs, code analysis
- **Filesystem**: Secure file access

### Data
- **PostgreSQL**: Database queries
- **MongoDB**: NoSQL operations
- **Memory**: Knowledge graph storage

### Productivity
- **Slack**: Team communication
- **Notion**: Workspace integration
- **Google Drive**: Cloud storage

### IoT
- **ThingsPanel**: IoT platform integration
- **Weather**: Forecasts and alerts
- **MQTT Bridge**: Device connectivity

### Cloud
- **Azure**: Microsoft cloud services
- **Cloudflare**: Edge computing
- **AWS** (community): Amazon services

---

## Performance Targets (IoT)

### Resource Constraints
- **Memory**: < 100KB footprint
- **Response Time**: < 500ms
- **CPU**: Efficient processing
- **Network**: Minimize bandwidth

### Optimization Techniques
- Lightweight JSON parsing
- Request batching
- Compression (gzip)
- Local caching
- Connection reuse

### Reliability
- Offline operation support
- Queue-based messaging
- Retry with exponential backoff
- Health checks
- Circuit breaker patterns

---

## Cloud Deployment Options

### Google Cloud Run
- **Guide**: https://cloud.google.com/run/docs/host-mcp-servers
- Containerized deployment
- Auto-scaling
- Regional availability

### AWS
- **Guide**: https://aws.amazon.com/solutions/guidance/deploying-model-context-protocol-servers-on-aws/
- ECS/EKS orchestration
- WAF protection
- Multi-layer security

### Cloudflare
- **Guide**: https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- Workers platform
- Edge computing
- Auto CI/CD from Git

### Azure
- Container Apps
- Azure OpenAI integration
- Managed identity

### FastMCP Cloud
- **Site**: https://gofastmcp.com/deployment/fastmcp-cloud
- Fastest deployment
- Auto-deploy from Git
- PR previews

---

## Client Libraries

### Official SDKs
- TypeScript/JavaScript
- Python
- Java, Kotlin
- C# (.NET)
- Go, PHP, Ruby, Rust, Swift

### Community Libraries
- **FastMCP** (Python): Production-ready features
- **mcp-use** (Python/TS): 6-line agent creation
- **mcp-agent**: Workflow patterns

### Applications Supporting MCP
- Claude Desktop / Claude.ai
- GitHub Copilot
- Cursor IDE
- Windsurf (Codeium)
- Zed Editor
- Replit

---

## Common Use Cases

### IT Operations
- Equipment management
- Incident response
- Automated ticketing
- Resource provisioning

### Development
- Code analysis
- Repository management
- CI/CD automation
- Documentation generation

### Business Intelligence
- Data query and analysis
- Report generation
- Metric tracking
- Dashboard updates

### IoT & Smart Buildings
- Environmental monitoring
- HVAC control
- Energy optimization
- Predictive maintenance

### Manufacturing
- Equipment monitoring
- Quality control
- Supply chain optimization
- Downtime reduction

---

## Real-World Results

### Block (Square)
- Thousands of daily users
- **50-75% time savings** on common tasks
- Company-wide deployment
- Tool: Goose (MCP-compatible)

### German Automotive Manufacturer
- **25% reduction** in unplanned downtime
- **10% increase** in production efficiency
- Legacy equipment integration

### IoT-MCP Research
- **100% task success** rate (22 sensor types)
- **205ms** average response time
- **74KB** peak memory (6 MCU types)

---

## Development Workflow

### 1. Start Small
```bash
# Run a reference server
npx @modelcontextprotocol/server-filesystem /path/to/data

# Connect with Claude Desktop
# Add to config: claude_desktop_config.json
```

### 2. Build Custom Server
```typescript
// TypeScript example
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-iot-server",
  version: "1.0.0"
});

// Add tools, resources, prompts
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: [...] };
});
```

```python
# Python example with FastMCP
from fastmcp import FastMCP

mcp = FastMCP("my-iot-server")

@mcp.tool()
def read_sensor(sensor_id: str) -> dict:
    """Read data from IoT sensor"""
    return {"temp": 22.5, "humidity": 45}

mcp.run()
```

### 3. Test Locally
```bash
# Test with MCP inspector
npx @modelcontextprotocol/inspector node dist/index.js
```

### 4. Deploy to Production
```bash
# Containerize
docker build -t my-mcp-server .

# Deploy to cloud
gcloud run deploy --source .
```

---

## Monitoring & Observability

### Key Metrics
- Request/response latency
- Error rates
- Tool call success rate
- Resource utilization (CPU, memory, network)
- Connected clients
- Message throughput

### Logging Best Practices
- Structured logging (JSON)
- Correlation IDs
- Appropriate log levels
- Sensitive data redaction
- Centralized aggregation

### Alerting
- Performance degradation
- Security anomalies
- Connectivity issues
- Error thresholds
- Resource exhaustion

---

## Troubleshooting

### Common Issues

**Connection Failures**
- Check transport configuration (stdio vs HTTP)
- Verify firewall rules
- Validate TLS certificates
- Check network connectivity

**Authentication Errors**
- Verify token validity
- Check OAuth configuration
- Validate session IDs
- Review access controls

**Performance Issues**
- Enable request batching
- Implement caching
- Optimize JSON parsing
- Check resource limits

**IoT-Specific**
- MQTT broker connectivity
- Device firmware compatibility
- Edge server resources
- Network latency

---

## Future Roadmap (2025)

### Upcoming Features
- Enhanced OAuth support
- Request batching improvements
- Stateful connections
- Streaming enhancements
- Tool namespacing

### Registry Development
- Official MCP Registry (GA late 2025)
- Versioning and discovery
- Certification program
- Security verification

### New Capabilities
- Image, audio, video context
- Industry-specific extensions
- Enhanced access control
- Improved monitoring tools

### Governance
- Potential move to independent foundation
- Community-driven development
- Open standards process

---

## Best Practices Summary

### Architecture
1. Use appropriate transport (stdio for local, HTTP for cloud, MQTT for IoT)
2. Implement defense-in-depth security
3. Design for failure (retries, circuit breakers)
4. Monitor everything
5. Document thoroughly

### Security
1. Always use TLS
2. Implement OAuth 2.0
3. Validate all inputs/outputs
4. Regular security updates
5. Audit and logging

### Performance
1. Optimize for target environment
2. Batch requests when possible
3. Cache aggressively
4. Monitor and alert
5. Load test before production

### IoT-Specific
1. Use MCP over MQTT for devices
2. Deploy edge servers when possible
3. Optimize for resource constraints
4. Implement offline operation
5. Test with real hardware early

---

## Getting Help

### Documentation
- Official docs: https://modelcontextprotocol.io/
- Claude docs: https://docs.anthropic.com/en/docs/agents-and-tools/mcp
- Specification: https://modelcontextprotocol.io/specification/

### Community
- GitHub Discussions: https://github.com/orgs/modelcontextprotocol/discussions
- Example servers: https://modelcontextprotocol.io/examples
- Awesome lists: Multiple curated collections on GitHub

### Courses
- Microsoft MCP for Beginners: https://github.com/microsoft/mcp-for-beginners
- Hugging Face MCP Course: https://huggingface.co/learn/mcp-course/
- DataCamp Tutorial: https://www.datacamp.com/tutorial/mcp-model-context-protocol

---

*Quick Reference Updated: 2025-11-17*
*Protocol Version: 2025-06-18*
