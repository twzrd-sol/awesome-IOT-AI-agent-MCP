/**
 * MCP IoT Server Example
 * Model Context Protocol server for IoT device management
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Mock IoT device database
const devices = new Map<string, any>([
  ["sensor-001", { temperature: 22.5, humidity: 65, status: "online" }],
  ["sensor-002", { temperature: 24.1, humidity: 70, status: "online" }],
  ["actuator-001", { state: "off", power: 0 }],
]);

// Create MCP server
const server = new Server(
  {
    name: "iot-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "read_sensor",
        description: "Read IoT sensor values",
        inputSchema: {
          type: "object",
          properties: {
            device_id: {
              type: "string",
              description: "Device identifier (e.g., sensor-001)",
            },
          },
          required: ["device_id"],
        },
      },
      {
        name: "control_actuator",
        description: "Control IoT actuator",
        inputSchema: {
          type: "object",
          properties: {
            device_id: {
              type: "string",
              description: "Actuator identifier",
            },
            action: {
              type: "string",
              enum: ["on", "off", "toggle"],
              description: "Action to perform",
            },
          },
          required: ["device_id", "action"],
        },
      },
      {
        name: "list_devices",
        description: "List all IoT devices",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "read_sensor": {
      const device = devices.get(args.device_id);
      if (!device) {
        return {
          content: [
            {
              type: "text",
              text: `Error: Device ${args.device_id} not found`,
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                device_id: args.device_id,
                temperature: device.temperature,
                humidity: device.humidity,
                status: device.status,
                timestamp: new Date().toISOString(),
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "control_actuator": {
      const device = devices.get(args.device_id);
      if (!device) {
        return {
          content: [
            {
              type: "text",
              text: `Error: Device ${args.device_id} not found`,
            },
          ],
        };
      }

      let newState: string;
      switch (args.action) {
        case "on":
          newState = "on";
          device.power = 100;
          break;
        case "off":
          newState = "off";
          device.power = 0;
          break;
        case "toggle":
          newState = device.state === "on" ? "off" : "on";
          device.power = newState === "on" ? 100 : 0;
          break;
        default:
          newState = device.state;
      }

      device.state = newState;
      devices.set(args.device_id, device);

      return {
        content: [
          {
            type: "text",
            text: `Actuator ${args.device_id} ${args.action}: ${newState} (power: ${device.power}%)`,
          },
        ],
      };
    }

    case "list_devices": {
      const deviceList = Array.from(devices.entries()).map(([id, data]) => ({
        id,
        ...data,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                total_devices: devices.size,
                devices: deviceList,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    default:
      return {
        content: [
          {
            type: "text",
            text: `Error: Unknown tool ${name}`,
          },
        ],
      };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("IoT MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
