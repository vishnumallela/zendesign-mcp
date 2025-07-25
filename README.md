# Zendesign MCP Server



## Setup and Installation

### Prerequisites
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone or download this repository
2. Install dependencies using uv:
```bash
uv sync
```

## Running the Server

To start the MCP server:

```bash
uv run python server.py
```

The server will start on port 9000 using Server-Sent Events (SSE) transport.

You should see output indicating the server is running:
```
FastMCP server running on port 9000
```

## Adding to Cursor

To use this MCP server with Cursor, you need to configure it in your Cursor settings:

### Method 1: Via Cursor Settings UI

1. Open Cursor
2. Go to **Cursor Settings** (⌘+, on Mac or Ctrl+, on Windows/Linux)
3. Navigate to **Features** → **Beta** → **Model Context Protocol**
4. Add a new MCP server with the following configuration:
   - **Name**: `Zendesign`
   - **Command**: `uv`
   - **Arguments**: `["run", "python", "server.py"]`
   - **Working Directory**: `/path/to/your/zd-mcp` (replace with your actual project path)

### Method 2: Via Configuration File

Add the following to your Cursor MCP configuration file:

```json
{
  "mcpServers": {
    "zendesign": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/your/zd-mcp"
    }
  }
}
```

**Note**: Replace `/path/to/your/zd-mcp` with the actual absolute path to your project directory.

### Verification

After adding the server to Cursor:

1. Restart Cursor
2. The Zendesign MCP server should appear in your available tools
3. You can now ask Cursor questions about Zendesign components, and it will use the MCP server to fetch real-time information

### Example Usage in Cursor

Once configured, you can interact with the Zendesign design system through Cursor:

- "Show me the button component from Zendesign"
- "What are the styling options for the card component?"
- "Get the design system guidelines from Zendesign"

## Troubleshooting

### Server Won't Start
- Ensure all dependencies are installed: `uv sync`
- Check that port 9000 is not in use by another application
- Verify Python version compatibility

### Cursor Can't Connect
- Ensure the server is running before starting Cursor
- Verify the working directory path is correct in your MCP configuration
- Check Cursor's MCP logs for connection errors

### Component Not Found
- Verify the component name is correct (e.g., 'button', 'card', 'input')
- Check that the Zendesign API is accessible from your network

## Development

This server uses:
- **FastMCP**: For MCP protocol implementation
- **requests**: For HTTP API calls to Zendesign
- **asyncio**: For asynchronous operations

To modify or extend the server, edit `server.py` and restart the server for changes to take effect.
