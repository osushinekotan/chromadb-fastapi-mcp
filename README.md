## Installation

1. Clone the repository
2. Install dependencies:
   ```
   uv sync
   ```
3. Copy `.env.example` to `.env` and configure settings:
   ```
   cp .env.example .env
   ```
4. Edit `.env` with your preferred settings

## Configuration

Configure the following environment variables in your `.env` file:

- `CHROMA_CLIENT_TYPE`: Either `ephemeral` or `persistent`
- `CHROMA_DATA_DIR`: Directory for storage when using persistent client
- `OPENAI_API_KEY`: Your OpenAI API key for embeddings

## Usage

Run the server:

```bash
cd /path/to/chromadb-fastapi-mcp
uv run python -m app.main
```

Or with uvicorn directly:

```bash
uv run uvicorn app.main:app --reload
```

The server will start at http://localhost:8000, and API documentation is available at http://localhost:8000/docs.

## API Endpoints

### Collections

- `GET /api/collections/` - List all collections
- `POST /api/collections/` - Create a new collection
- `GET /api/collections/{collection_name}/peek` - Peek at documents in a collection
- `GET /api/collections/{collection_name}/info` - Get collection information
- `GET /api/collections/{collection_name}/count` - Get document count in a collection
- `PUT /api/collections/{collection_name}` - Modify a collection
- `DELETE /api/collections/{collection_name}` - Delete a collection

### Documents

- `POST /api/documents/add` - Add documents to a collection
- `POST /api/documents/query` - Query documents from a collection
- `POST /api/documents/get` - Get documents from a collection
- `PUT /api/documents/update` - Update documents in a collection
- `DELETE /api/documents/delete` - Delete documents from a collection

## MCP server

https://github.com/tadata-org/fastapi_mcp

### Connecting to the MCP Server using SSE

Once your FastAPI app with MCP integration is running, you can connect to it with any MCP client supporting SSE, such as Cursor:

1. Run your application.

2. In Cursor -> Settings -> MCP, use the URL of your MCP server endpoint (e.g., `http://localhost:8000/mcp`) as sse.

3. Cursor will discover all available tools and resources automatically.

### Connecting to the MCP Server using [mcp-proxy stdio](https://github.com/sparfenyuk/mcp-proxy?tab=readme-ov-file#1-stdio-to-sse)

If your MCP client does not support SSE, for example Claude Desktop:

1. Run your application.

2. Install [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy?tab=readme-ov-file#installing-via-pypi), for example: `uv tool install mcp-proxy`.

3. Add in Claude Desktop MCP config file (`claude_desktop_config.json`):

On Windows:
```json
{
  "mcpServers": {
    "my-api-mcp-proxy": {
        "command": "mcp-proxy",
        "args": ["http://127.0.0.1:8000/mcp"]
    }
  }
}
```
On MacOS:

Find the path to mcp-proxy by running in Terminal: `which mcp-proxy`.
```json
{
  "mcpServers": {
    "my-api-mcp-proxy": {
        "command": "/Full/Path/To/Your/Executable/mcp-proxy",
        "args": ["http://127.0.0.1:8000/mcp"]
    }
  }
}
```


Find the path to mcp-proxy by running in Terminal: `which uvx`.
```json
{
  "mcpServers": {
    "my-api-mcp-proxy": {
        "command": "/Full/Path/To/Your/uvx",
        "args": ["mcp-proxy", "http://127.0.0.1:8000/mcp"]
    }
  }
}
```

4. Claude Desktop will discover all available tools and resources automatically
