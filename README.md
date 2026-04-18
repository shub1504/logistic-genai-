<div align="center">

# 🚀 Delhi Logistics Optimizer

### AI-Powered Multi-Stop Delivery Route Optimization

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini_ADK-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Claude](https://img.shields.io/badge/Anthropic-Claude_AI-D4A96A?style=for-the-badge)](https://anthropic.com)
[![BigQuery](https://img.shields.io/badge/BigQuery-Logged-185ABC?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Type plain English. Get an optimized Delhi delivery route. Powered by Dijkstra, Nearest Neighbor, 2-opt, Claude AI, Google Gemini ADK, and BigQuery.**

<br/>

```
You:  "deliver to Saket, Rohini and Dwarka today"

[Pipeline] Extracting locations via Claude AI...
[Pipeline] Extracted: ['Saket, New Delhi', 'Rohini, New Delhi', 'Dwarka, New Delhi']
[Pipeline] Building distance matrix...
[Pipeline] Optimizing route → Nearest Neighbor + 2-opt...
[Pipeline] Optimized: Connaught Place → Lajpat Nagar → Saket → Dwarka → Rohini → Connaught Place
[Pipeline] Distance: 86.9 km  |  Stops: 4  |  Algorithm: 2-opt improved (cost 19 → 14, ↓26%)
[BigQuery] Route logged ✅
```

</div>

---

## 📌 Table of Contents

- [What It Does](#-what-it-does)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Algorithms](#-algorithms-the-core-dsa)
- [Architecture](#-system-architecture)
- [Setup & Installation](#-setup--installation)
- [Running the Project](#-running-the-project)
- [ADK Web Agent](#-adk-web-agent)
- [BigQuery Integration](#-bigquery-integration)
- [MCP Server](#-mcp-server)
- [Industry Comparison](#-industry-comparison)
- [API Keys Required](#-api-keys-required)

---

## ✨ What It Does

This project is a **full-stack logistics optimizer** that combines classical computer science algorithms with modern generative AI:

| Feature | Description |
|---|---|
| 🧠 **NL Location Extraction** | Type `"deliver to Saket and Rohini"` — Claude AI extracts the locations |
| 🗺️ **Route Optimization** | Dijkstra + Nearest Neighbor + 2-opt finds the mathematically optimal delivery order |
| 📊 **BigQuery Logging** | Every optimized route is stored in Google BigQuery for analytics |
| 🤖 **Conversational Agent** | Google ADK + Gemini lets you query routes in natural language |
| 🔌 **MCP Server** | Custom Model Context Protocol server connects AI agent to BigQuery |
| 🗃️ **Mock Mode** | Runs fully offline with Delhi mock data — no API costs for demos |

---

## 📁 Project Structure

```
logistic-genai/
│
├── 📄 main.py                        ← CLI entry point + ADK launcher
├── 📄 pipeline.py                    ← End-to-end pipeline (connects all 6 layers)
├── 📄 config.py                      ← API keys and settings loader
├── 📄 mcp_server.py                  ← BigQuery MCP Server (JSON-RPC protocol)
├── 📄 requirements.txt               ← All Python dependencies
├── 📄 .env.example                   ← Template for environment variables
├── 📄 .gitignore                     ← Excludes .env and service_account.json
│
├── 🧮 algorithms/
│   ├── __init__.py
│   ├── graph.py                      ← Weighted directed graph (adjacency list)
│   ├── dijkstra.py                   ← Dijkstra's shortest path + path reconstruction
│   └── nearest_neighbour.py          ← Nearest Neighbor TSP + 2-opt improvement
│
├── 🤖 agent/
│   ├── __init__.py
│   ├── extractor.py                  ← Claude AI location extractor from plain English
│   ├── explainer.py                  ← Claude AI route briefing + manager summary
│   └── prompts.py                    ← All GenAI prompt templates
│
├── ☁️ services/
│   ├── __init__.py
│   ├── geocoding.py                  ← Google Maps Geocoding API
│   ├── distance_matrix.py            ← Google Maps Distance Matrix API (km + minutes)
│   ├── mock_data.py                  ← Delhi mock locations + distance matrix (offline)
│   ├── bigquery_logger.py            ← Log routes to BigQuery + fetch history
│   └── bigquery_public.py            ← Query public BQ datasets (NYC taxi, air quality)
│
├── 🌐 logistics_agent_app/
│   ├── __init__.py
│   ├── agent.py                      ← Google ADK agent with 4 BigQuery tools
│   └── .env                          ← Gemini API key for ADK
│
└── 🧪 tests/
    ├── test_setup2.py                ← Phase 2: Algorithm tests
    └── test_phase5.py                ← Phase 5: BigQuery integration tests
```

---

## 🛠️ Tech Stack

### Core Algorithms (Built from Scratch)
| Algorithm | File | Time Complexity | Purpose |
|---|---|---|---|
| Weighted Directed Graph | `algorithms/graph.py` | O(1) add edge | Store locations + road distances |
| Dijkstra's Shortest Path | `algorithms/dijkstra.py` | O((V+E) log V) | Shortest path between any two stops |
| Nearest Neighbor Heuristic | `algorithms/nearest_neighbour.py` | O(n²) | Build initial multi-stop route |
| 2-opt Local Search | `algorithms/nearest_neighbour.py` | O(n²) per iter | Improve route (↓26% in demo) |

### AI & Generative AI
| Component | Technology | Purpose |
|---|---|---|
| Location Extractor | Claude API (claude-sonnet-4) | Parse delivery stops from plain English |
| Route Explainer | Claude API | Generate driver briefing + manager summary |
| Conversational Agent | Google ADK + Gemini 2.5 Flash | Natural language route queries |
| Agent Tools | Google FunctionTool | Expose BigQuery functions to Gemini |

### Google Cloud
| Service | Purpose |
|---|---|
| BigQuery | Store + query all optimized routes |
| Maps Geocoding API | Convert address strings to lat/lng |
| Maps Distance Matrix API | Real Delhi road distances (km) + travel times (min) |
| Vertex AI | Gemini model backend for ADK |
| Cloud Run | Deployment target (Dockerfile included) |

### Infrastructure
| Tool | Purpose |
|---|---|
| Google ADK | Build and run the conversational agent web UI |
| MCP Server (custom) | JSON-RPC protocol server exposing BigQuery to AI |
| python-dotenv | Secure API key management |
| heapq | Min-heap priority queue for Dijkstra |

---

## 🧮 Algorithms: The Core DSA

### Why These Algorithms?

Google Maps solves **A → B** (Single Source Shortest Path).  
This project solves **A → B → C → D → A** (Travelling Salesman Problem — NP-Hard).

These are fundamentally different problems requiring different algorithmic approaches.



### The TSP Problem

```
For n delivery stops → n! possible routes

5  stops =          120 routes  ← manageable
10 stops =    3,628,800 routes  ← very slow  
20 stops = 2.4 × 10¹⁸ routes   ← impossible

Nearest Neighbor + 2-opt gives near-optimal in O(n²)
Same approach used by Amazon, Swiggy, Blinkit at scale
```

---

## 🏗️ System Architecture

```
                    ┌─────────────────────────────┐
                    │   User: plain English input  │
                    │  "deliver to Saket, Rohini"  │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Claude AI (Extractor)      │
                    │   Pulls location names       │
                    │   from natural language      │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Google Maps APIs           │
                    │   Geocoding + Distance       │
                    │   Matrix (or Mock Data)      │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────▼──────────────────────┐
              │           Custom Graph (adjacency list)    │
              │   Nodes = locations | Edges = distances    │
              └────────────────────┬──────────────────────┘
                                   │
        ┌──────────────────────────▼──────────────────────────────┐
        │                   Optimization Pipeline                  │
        │  Dijkstra (all-pairs) → Nearest Neighbor → 2-opt        │
        │  O((V+E)logV)          O(n²)               O(n²/iter)   │
        └──────────────────────────┬──────────────────────────────┘
                                   │
              ┌────────────────────▼──────────────────────┐
              │           Claude AI (Explainer)            │
              │   Driver briefing + Manager summary        │
              └────────────────────┬──────────────────────┘
                                   │
              ┌────────────────────▼──────────────────────┐
              │           Google BigQuery Logger           │
              │   Stores route, distance, stops, algo      │
              └────────────────────┬──────────────────────┘
                                   │
              ┌────────────────────▼──────────────────────┐
              │     Google ADK Agent (Gemini 2.5 Flash)   │
              │   "Show me routes" / "Average distance?"  │
              │   Queries BigQuery via MCP protocol        │
              └───────────────────────────────────────────┘
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Google Cloud account with billing enabled
- Anthropic API key
- Google AI Studio API key (for ADK)

### 1. Clone the repository

```bash
git clone https://github.com/shub1504/logistic-genai.git
cd logistic-genai
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your actual keys:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_key
GOOGLE_CLOUD_PROJECT=your_project_id
BIGQUERY_DATASET=logistics_data
GOOGLE_CLOUD_REGION=us-central1
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_APPLICATION_CREDENTIALS=service_account.json
USE_MOCK=true
```

### 5. Enable Google Cloud APIs

In Google Cloud Console, enable:
- ✅ Maps Geocoding API
- ✅ Maps Distance Matrix API
- ✅ BigQuery API
- ✅ Vertex AI API

### 6. Download service account key

IAM & Admin → Service Accounts → Create → BigQuery Admin role → Download JSON → rename to `service_account.json`

---

## ▶️ Running the Project

### Option 1: Interactive CLI

```bash
python main.py
```

```
============================================================
  DELHI LOGISTICS OPTIMIZER
  Powered by Dijkstra + Gemini + BigQuery
============================================================
  You: deliver to Saket, Rohini and Dwarka today
```

### Option 2: Single message

```bash
python main.py --message "deliver to Saket, Rohini and Dwarka today"
```

### Option 3: Run tests

```bash
# Test algorithms (Phase 2)
python test_setup2.py

# Test BigQuery integration (Phase 5)
python test_phase5.py
```

---

## 🌐 ADK Web Agent

The conversational agent lets you query your delivery data in natural language.

### Start the agent

```bash
# Install ADK
pip install google-adk

# Configure logistics_agent_app/.env
echo "GOOGLE_GENAI_USE_VERTEXAI=0" > logistics_agent_app/.env
echo "GOOGLE_API_KEY=your_gemini_key" >> logistics_agent_app/.env

# Launch web UI
adk web "C:\path\to\logistic-genai"
```

Open `http://127.0.0.1:8000` and select `logistics_agent_app`.

### Example queries

```
"Show me the most recent delivery routes"
"What is the average delivery distance across all routes?"
"Find all routes that include Saket"
"Optimize a route for Connaught Place, Saket, Rohini and Dwarka"
```

### Agent Tools

| Tool | Description |
|---|---|
| `get_recent_routes` | Fetch latest routes from BigQuery |
| `get_route_statistics` | Avg/max/min distance, total routes |
| `find_routes_by_location` | Search routes containing a stop |
| `optimize_delivery_route` | Run Nearest Neighbor + 2-opt live |

---

## 📊 BigQuery Integration

Every optimized route is automatically logged to BigQuery.

### Schema: `logistics_data.routes`

| Column | Type | Description |
|---|---|---|
| `run_id` | STRING | Unique route identifier (UUID) |
| `timestamp` | TIMESTAMP | When route was optimized |
| `route` | STRING | JSON array of ordered stops |
| `total_distance` | FLOAT | Total km for full round trip |
| `num_stops` | INTEGER | Number of delivery stops |
| `algorithm` | STRING | Algorithm used |
| `user_message` | STRING | Original user input |
| `briefing` | STRING | AI-generated driver briefing |



---

## 🔌 MCP Server

The custom MCP (Model Context Protocol) server exposes BigQuery as tools for AI agents.

### Start the server

```bash
python mcp_server.py
```

### Available tools

| Tool | Description |
|---|---|
| `bigquery_query` | Run any SQL query on your logistics data or public datasets |
| `bigquery_list_tables` | List all tables in `logistics_data` |
| `bigquery_get_schema` | Get column schema for any table |

### Antigravity / VS Code integration

```json
{
  "mcpServers": {
    "bigquery-logistics": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "C:\\path\\to\\logistic-genai"
    }
  }
}
```

---

## 🏭 Industry Comparison

| Feature | Blinkit | Amazon | Our Optimizer |
|---|---|---|---|
| Routing Algorithm | A* + Google Maps | VRP + DeepFleet ML | Dijkstra + Nearest Neighbor + 2-opt |
| Multi-stop optimization | ❌ Single stop | ✅ Full VRP | ✅ TSP (academic) |
| Natural language input | ❌ | ❌ | ✅ Claude AI |
| Conversational agent | ❌ | ❌ | ✅ Google ADK |
| Route history | ✅ Internal | ✅ AWS | ✅ BigQuery |
| From-scratch algorithms | ❌ | ❌ | ✅ |
| Real-time traffic | ✅ | ✅ | ❌ (upgradable) |

> Our optimizer implements the same algorithmic core (Dijkstra + TSP heuristics) that powers billion-dollar delivery systems — with the addition of a modern natural language interface that neither Blinkit nor Amazon currently offers their fleet managers.

---

## 🔑 API Keys Required

| Key | Where to get | Used for |
|---|---|---|
| `GOOGLE_MAPS_API_KEY` | [console.cloud.google.com](https://console.cloud.google.com) → Credentials | Geocoding + Distance Matrix |
| `GOOGLE_CLOUD_PROJECT` | Your GCP project ID | BigQuery + Vertex AI |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Claude AI location extraction |
| `GOOGLE_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Gemini ADK agent |
| `service_account.json` | GCP → IAM → Service Accounts → Keys | BigQuery authentication |

> ⚠️ Never commit `.env` or `service_account.json` to GitHub. Both are in `.gitignore`.

---

## 📈 Results

```
Algorithm Demo (test_setup2.py):
  Shortest path Depot → WH-3:  ['Depot', 'WH-2', 'WH-3']  cost = 5
  Nearest Neighbor route cost:  19.0
  After 2-opt improvement:      14    ← 26% better ✅

Delhi Pipeline Demo:
  Input:    "deliver to Saket, Rohini and Dwarka today"
  Route:    Connaught Place → Lajpat Nagar → Saket → Dwarka → Rohini → Connaught Place
  Distance: 86.9 km
  Logged:   ✅ BigQuery
```



