# Orbital Foundry — Self-Evolving Predictive Maintenance Platform

Real-time anomaly detection for industrial machines using Z-score analysis, Isolation Forest, and polyfit trend scoring. Includes a Streamlit monitoring agent, FastAPI backend, React dashboard, and an Express.js SSE simulation server.

## Live Deployments

| Service | URL |
|---|---|
| Frontend (Vercel) | https://ai-predictive-maintainance.vercel.app |
| Backend API (Render) | https://ai-predictive-maintainance.onrender.com |
| Live Server (Railway) | https://aipredictivemaintainance-production.up.railway.app |

---

## Architecture

```
orbital-foundry/
├── backend/               ← FastAPI API + Streamlit agent + ML models
│   ├── api/
│   │   └── main.py        ← FastAPI server (port 8000)
│   ├── agents/
│   │   └── app.py         ← Streamlit monitoring UI
│   ├── ml/                ← Standalone ML utility scripts
│   ├── data/              ← baselines.json, sensor_history.csv, predictions_log.csv
│   ├── models/            ← Trained IsolationForest .pkl files
│   ├── requirements.txt
│   ├── .env.example
│   ├── Procfile           ← Render/Railway deploy config
│   └── runtime.txt
├── frontend/              ← React + Vite + TailwindCSS dashboard (port 5173)
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   │   └── useMachines.js   ← SSE consumer hook
│   │   └── data/
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── vercel.json        ← Vercel deploy config
├── live_server/           ← Express.js SSE simulation server (port 3000)
│   ├── server.js
│   ├── generate-history.js
│   ├── public/index.html  ← Built-in web dashboard
│   ├── package.json
│   ├── .env.example
│   └── railway.toml       ← Railway deploy config
├── .gitignore
├── package.json           ← Root: `npm run dev` starts all 3 services
└── README.md
```

---

## Quick Start (3 Terminals)

### Prerequisites

- **Node.js** >= 18
- **Python** >= 3.11
- **pip** (or venv)

---

### Terminal 1 — Live Server (SSE Simulation)

```bash
cd live_server
npm install
npm start
# Running at http://localhost:3000
# Dashboard at http://localhost:3000
```

---

### Terminal 2 — Backend (FastAPI)

```bash
cd backend

# Create and activate virtual environment (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Copy env file
cp .env.example .env

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Optional — Streamlit Agent** (replaces the React dashboard with a Streamlit UI):

```bash
# In the same backend venv:
streamlit run agents/app.py
# Opens at http://localhost:8501
```

---

### Terminal 3 — Frontend (React + Vite)

```bash
cd frontend
npm install

# Copy env file
cp .env.example .env

npm run dev
# Opens at http://localhost:5173
```

---

### One-Command Dev (requires `npm install` at root first)

```bash
npm install          # installs concurrently
npm run install:all  # installs node_modules in live_server/ and frontend/
npm run dev          # starts all 3 services in parallel
```

---

## Environment Variables

### `backend/.env`

| Variable | Default | Description |
|---|---|---|
| `LIVE_SERVER_URL` | `http://localhost:3000` | URL of the live/simulation SSE server |

### `frontend/.env`

| Variable | Default | Description |
|---|---|---|
| `VITE_API_URL` | `http://localhost:8000` | URL of the FastAPI backend |

### `live_server/.env`

| Variable | Default | Description |
|---|---|---|
| `PORT` | `3000` | Port the SSE server listens on |

---

## API Reference

### FastAPI Backend (`http://localhost:8000`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/machines` | All machine states |
| GET | `/api/machines/{id}` | Single machine state |
| GET | `/api/machines/{id}/history?n=30` | Last N sensor readings |
| GET | `/api/stream` | SSE stream of machine updates |
| POST | `/api/machines/{id}/confirm` | Confirm an alert |
| POST | `/api/machines/{id}/dismiss` | Dismiss an alert |
| GET | `/api/alerts` | Last 20 alerts |

### Live Server (`http://localhost:3000`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/stream/{machine_id}` | SSE stream, 1 reading/sec |
| GET | `/history/{machine_id}` | 7-day historical data |
| POST | `/alert` | Register an alert |
| POST | `/schedule-maintenance` | Book a maintenance slot |
| GET | `/alerts` | All raised alerts |
| GET | `/machines` | Machine IDs and baselines |

---

## Machines Monitored

| ID | Name | Bay | Fault Pattern |
|---|---|---|---|
| CNC_01 | Precision CNC Mill | A-1 | Bearing wear (vibration + temp ramp) |
| CNC_02 | Kinetic Robotic Arm | A-2 | Thermal runaway (afternoon spikes) |
| PUMP_03 | Hydraulic Pump | B-1 | Cavitation bursts + RPM decline |
| CONVEYOR_04 | Belt Conveyor System | C-1 | Mostly healthy, occasional spikes |

---

## Deployment

### Frontend → Vercel

```bash
# Install Vercel CLI
npm i -g vercel

cd frontend
cp .env.example .env
# Set VITE_API_URL to your deployed backend URL

vercel
# Follow prompts — vercel.json is already configured
```

### Backend → Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set **Root Directory** to `backend`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `LIVE_SERVER_URL=<your live server URL>`

> `Procfile` is included as an alternative start method.

### Live Server → Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

cd live_server
railway login
railway init
railway up
# railway.toml configures the start command automatically
```

Or deploy via the Railway dashboard:
1. New project → Deploy from GitHub
2. Set **Root Directory** to `live_server`
3. Railway auto-detects `railway.toml`

---

## ML Utilities (`backend/ml/`)

| Script | Purpose |
|---|---|
| `baseline_builder.py` | Rebuild baselines.json + retrain IsolationForest models from sensor_history.csv |
| `rebuild_baselines.py` | Rebuild baselines from live server `/history` endpoint |
| `anomaly_detector.py` | Standalone CSV watcher with Z-score + IF detection |
| `metrics_calculator.py` | F1, precision, recall, FPR, MCC from predictions_log.csv |
| `confusion_matrix.py` | Confusion matrix visualization |
| `sensor_simulator.py` | Generate synthetic sensor data CSV |

Run any from the `backend/` directory:

```bash
cd backend
python ml/baseline_builder.py
python ml/metrics_calculator.py
```

---

## Git Commands

```bash
# Stage and commit the restructured project
git add .
git commit -m "Restructure into backend/, frontend/, live_server/ monorepo"

# Push to GitHub
git push origin main
```
