# Delhi Logistics Optimizer 🚀

A full-stack AI-powered logistics route optimization system combining 
**Data Structures & Algorithms** with **Generative AI** and **Google Cloud**.

## What it does
- Extracts delivery locations from plain English using Claude AI
- Optimizes multi-stop Delhi delivery routes using Dijkstra + Nearest Neighbor + 2-opt
- Logs every route to Google BigQuery
- Provides a conversational agent via Google ADK + Gemini

## Tech Stack
- **Algorithms:** Dijkstra, Nearest Neighbor, 2-opt (built from scratch)
- **AI:** Claude API (Anthropic) + Google Gemini via ADK
- **Cloud:** Google BigQuery + Google Maps APIs
- **Agent:** Google Agent Development Kit (ADK) + MCP Server

## Project Structure
logistic-genai/
├── algorithms/          ← Dijkstra, Nearest Neighbor, 2-opt
├── agent/               ← Claude AI extractor + explainer
├── services/            ← Google Maps, BigQuery, mock data
├── logistics_agent_app/ ← Google ADK web agent
├── pipeline.py          ← End-to-end pipeline
├── main.py              ← CLI entry point
└── mcp_server.py        ← BigQuery MCP server

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   CLAUDE_API_KEY=your_claude_key_here
   GOOGLE_MAPS_API_KEY=your_maps_key_here
   GOOGLE_CLOUD_PROJECT=your_gcp_project
   GOOGLE_CLOUD_REGION=us-central1
   BIGQUERY_DATASET=logistics_data
   ```

3. **Enable BigQuery API:**
   ```bash
   gcloud services enable bigquery.googleapis.com
   ```

4. **Create BigQuery dataset:**
   ```bash
   python services/bigquery_setup.py
   ```

5. **Run the pipeline:**
   ```bash
   python pipeline.py
   ```

6. **Run the ADK agent:**
   ```bash
   python logistics_agent_app/agent.py
   ```
   Then open `http://localhost:3000` in your browser.

## Usage

### Extract locations with Claude AI
```bash
python agent/extractor.py "I need to deliver packages to Saket, Rohini, Dwarka, and Connaught Place."
```

### Optimize a route
```bash
python main.py "Saket, Rohini, Dwarka, Connaught Place, Lajpat Nagar"
```

### View recent routes
```bash
python main.py --list-routes
```

### Get route statistics
```bash
python main.py --stats
```

### Search by location
```bash
python main.py --search Rohini
```

## Algorithms Explained

### Dijkstra's Algorithm
Finds the shortest path from a single source to all other nodes in a weighted graph.
- Used to build the complete distance matrix from Google Maps API
- Finds shortest paths between all pairs of locations

### Nearest Neighbor Heuristic
Greedy algorithm that builds a route by repeatedly choosing the nearest unvisited location.
- Fast and simple
- Good for initial route construction
- Not guaranteed to be optimal

### 2-opt Local Search
Improves an existing route by reversing segments that reduce total distance.
- Iteratively swaps edges to find better routes
- Significantly improves nearest neighbor solutions
- Guaranteed to terminate but can get stuck in local optima

## BigQuery Schema

### routes table
| Column | Type | Description |
|--------|------|-------------|
| run_id | STRING | Unique identifier for the run |
| timestamp | TIMESTAMP | When the route was optimized |
| route | JSON | Ordered list of stops |
| total_distance | FLOAT | Total distance in km |
| num_stops | INTEGER | Number of stops (excluding start/end) |
| algorithm | STRING | Algorithm used (e.g., "Nearest Neighbor + 2-opt") |

