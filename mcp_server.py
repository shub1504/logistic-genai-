# mcp_server.py

"""
MCP (Model Context Protocol) server for BigQuery.
Exposes your BigQuery dataset + public datasets as tools
that Claude can call directly in natural language.

Start it with:  python mcp_server.py
Then register it in Antigravity's MCP settings.
"""

import json
import sys
from google.cloud import bigquery
from config import GCP_PROJECT, BQ_DATASET, BQ_LOCATION

client = bigquery.Client(project=GCP_PROJECT, location=BQ_LOCATION)


# ── Tool implementations ──────────────────────────────────────────

def run_query(sql: str, max_rows: int = 50) -> str:
    """Execute any SQL query and return results as a JSON string."""
    try:
        results = client.query(sql).result()
        rows    = [dict(row) for row in results][:max_rows]
        return json.dumps(rows, default=str, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def list_tables() -> str:
    """List all tables in the logistics dataset."""
    try:
        tables = list(client.list_tables(f"{GCP_PROJECT}.{BQ_DATASET}"))
        return json.dumps([t.table_id for t in tables])
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_schema(table_name: str) -> str:
    """Return column names and types for a given table."""
    try:
        table  = client.get_table(f"{GCP_PROJECT}.{BQ_DATASET}.{table_name}")
        schema = [
            {"name": f.name, "type": f.field_type, "mode": f.mode}
            for f in table.schema
        ]
        return json.dumps(schema, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool definitions (shown to Claude) ───────────────────────────

TOOLS = [
    {
        "name": "bigquery_query",
        "description": (
            "Run a SQL query against BigQuery. "
            "Can query your own logistics routes dataset "
            f"(`{GCP_PROJECT}.{BQ_DATASET}`) "
            "OR public datasets such as "
            "`bigquery-public-data.openaq.global_air_quality` "
            "and `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {
                    "type":        "string",
                    "description": "The full SQL query to run"
                },
                "max_rows": {
                    "type":        "integer",
                    "description": "Maximum rows to return (default 50)"
                },
            },
            "required": ["sql"],
        },
    },
    {
        "name": "bigquery_list_tables",
        "description": (
            f"List all tables inside the {BQ_DATASET} logistics dataset."
        ),
        "inputSchema": {
            "type":       "object",
            "properties": {},
        },
    },
    {
        "name": "bigquery_get_schema",
        "description": "Get the column schema for a specific table in the logistics dataset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type":        "string",
                    "description": "Table name without project/dataset prefix e.g. 'routes'"
                },
            },
            "required": ["table_name"],
        },
    },
]


# ── MCP protocol loop ─────────────────────────────────────────────

def handle_message(msg: dict) -> dict | None:
    method = msg.get("method")
    msg_id = msg.get("id")

    # Handshake
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id":      msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities":    {"tools": {}},
                "serverInfo":      {
                    "name":    "bigquery-logistics",
                    "version": "1.0.0"
                },
            },
        }

    # Claude asks what tools are available
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id":      msg_id,
            "result":  {"tools": TOOLS},
        }

    # Claude calls a tool
    if method == "tools/call":
        tool = msg["params"]["name"]
        args = msg["params"].get("arguments", {})

        if tool == "bigquery_query":
            result = run_query(args["sql"], args.get("max_rows", 50))
        elif tool == "bigquery_list_tables":
            result = list_tables()
        elif tool == "bigquery_get_schema":
            result = get_schema(args["table_name"])
        else:
            result = json.dumps({"error": f"Unknown tool: {tool}"})

        return {
            "jsonrpc": "2.0",
            "id":      msg_id,
            "result": {
                "content": [{"type": "text", "text": result}]
            },
        }

    return None


def main():
    print("[MCP] BigQuery server running — waiting for input...", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg      = json.loads(line)
            response = handle_message(msg)
            if response:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()