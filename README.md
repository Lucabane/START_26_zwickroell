# 🛠️ ZwickRoell Data Intelligence Orchestrator
**START Hack 2026 Project** | Team **Inglorious BaSTART**

> An industrial analysis platform designed to query, compare, and monitor 31,000+ material test reports through a natural, deterministic, and transparent interface.

---

## 🏗️ Technical Architecture: "Deterministic MCP Orchestrator"

Unlike traditional "Agentic" approaches, we implemented a deterministic orchestration layer **aligned with Model Context Protocol (MCP) standards**:

1. **Intent Routing & Local Fallback**: High-performance request classification (JSON Mode) coupled with local heuristic logic. Our system mimics the MCP host-client separation, ensuring functionality even if the LLM fails.
2. **Standardized Tooling & Semantic Mapper**: We designed our data interface to be MCP-compliant in logic. Before querying MongoDB, a semantic pre-processor normalizes entities (Machines, Materials) and handles Automatic Unit Normalization, acting as the MCP Server layer between the LLM and the raw data.
3. **Explainable AI (XAI)**: Every response includes a Tool Trace showing precisely which data was extracted and which specific tool was executed, following the MCP transparency philosophy.

---

## 📂 Project Structure

```text
.
├── backend/
│   ├── api/                # FastAPI Endpoints (Chat, Data)
│   ├── models/             # Pydantic Schemas (Strict Validation)
│   ├── services/           
│   │   ├── llm_orchestrator.py # Brain (Routing & Fallback)
│   │   ├── semantic_mapper.py  # Semantic Normalization & Units
│   │   └── data_access_layer.py # MongoDB Interface
│   └── tools/              # Business Logic (Trend, Compare, Inspect, Find)
├── frontend/
│   ├── app/                # Next.js 15 App Router
│   ├── components/         # UI Components (Charts, Stats Cards)
│   │   └── response/       # Rich Rendering (Markdown GFM, ChartRenderer)
│   ├── globals.css         # Tailwind v4 Config (@plugin typography)
│   └── lib/                # API Client & Types
└── README.md
```

## 🚀 The "Golden Path" (Demo Scenario)

The demo was designed to showcase the system's robustness against real-world industrial data:

* **Search**: *"Show me 3 tests for steel"*
    * **Feature**: Numeric limit extraction and dynamic Markdown table rendering.
* **Inspect**: *"Inspect data structure for BAR 52"*
    * **Feature**: Zero-shot dynamic schema detection.
* **Compare**: *"Compare Standard force between BAR 52 and metal plate"*
    * **Feature**: **"Wow" Moment** - Automatic unit disparity detection (kN vs N) and real-time recalculation for a fair physical comparison.
* **Trend**: *"Show me the trend over time"*
    * **Feature**: Volatility Analysis - Real-time standard deviation calculation. If a spike (outlier) is detected, the system alerts the user about production instability.

---

## 💻 Installation & Setup

### 1. Backend (FastAPI)
*Requires Python 3.10+*

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Create a .env file with OPENAI_API_KEY and MONGO_URI
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Next.js)
*Requires Node.js 18+*

```bash
# Navigate to the web directory
cd frontend/web

# Install base dependencies
npm install

# Install rendering plugins (Markdown & Typography)
npm install @tailwindcss/typography react-markdown remark-gfm

# Run the development server
npm run dev
```

The application will be accessible at **[http://localhost:3000](http://localhost:3000)**.

---

## 🛠️ Tech Stack

* **Frontend**: Next.js 15 (App Router), Tailwind CSS v4, Recharts, React-Markdown.
* **Backend**: FastAPI, Pydantic v2, OpenAI GPT-4o-mini (Structured Outputs).
* **Data**: MongoDB (31k records).
* **Logic**: Stateless deterministic orchestration (Latency < 1.5s).

---

*Developed by Team **Inglorious BaSTART** for START Hack 2026.*
