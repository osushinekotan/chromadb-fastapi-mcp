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
