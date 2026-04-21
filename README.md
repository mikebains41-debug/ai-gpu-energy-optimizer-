# 🤖 AI GPU Energy Optimizer

[![Frontend](https://img.shields.io/badge/Frontend-Vercel-000000?style=flat-square&logo=vercel)](https://vercel.com)
[![Backend](https://img.shields.io/badge/Backend-Railway-0B0D0E?style=flat-square&logo=railway)](https://railway.app)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

> **Enterprise-grade real-time GPU monitoring & AI-driven energy optimization platform.**  
> Track utilization, power draw, thermal metrics, and carbon footprint across distributed GPU clusters with sub-second WebSocket streaming.

---

## 📑 Table of Contents
- [✨ Features](#-features)
- [🌐 Live Demo](#-live-demo)
- [🏗 Architecture](#-architecture)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📡 API Reference](#-api-reference)
- [📦 Deployment](#-deployment)
- [👤 Author & License](#-author--license)

---

## ✨ Features

| Category | Capabilities |
|----------|--------------|
| 📊 **Real-Time Telemetry** | Live WebSocket streaming of GPU utilization, temperature, power draw, and memory bandwidth |
| 🧠 **AI Optimization Engine** | Automated workload shifting, thermal throttling alerts, and cost-saving recommendations |
| 💰 **Financial Analytics** | Real-time ROI tracking, annual savings projections, and $/kWh efficiency modeling |
| 🌍 **Sustainability Metrics** | CO₂ reduction tracking, renewable energy percentage, and carbon offset equivalents |
| 🔔 **Smart Notifications** | Threshold-based alerts, anomaly detection, and actionable optimization prompts |
| 📱 **Responsive UI** | Mobile-first dashboard with interactive Recharts visualizations and dark-mode native design |

---

## 🌐 Live Demo

| Component | URL |
|-----------|-----|
| **Frontend Dashboard** | [https://vb9gyxmx-mikebains41gmailcom.vercel.app](https://vb9gyxmx-mikebains41gmailcom.vercel.app) |
| **Backend API** | [https://ai-gpu-energy-optimizer-production.up.railway.app](https://ai-gpu-energy-optimizer-production.up.railway.app) |
| **WebSocket Stream** | `wss://ai-gpu-energy-optimizer-production.up.railway.app/ws` |

**Quick Health Check:**
```bash
curl https://ai-gpu-energy-optimizer-production.up.railway.app/health
```

---

## 🏗 Architecture8
---

## 🛠 Tech Stack

### **Frontend**
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS + `clsx` / `tailwind-merge`
- **State:** React Hooks (`useState`, `useEffect`, `useRef`)
- **Charts:** Recharts 2.12+
- **Icons:** Lucide React
- **Hosting:** Vercel (Edge Network)

### **Backend**
- **Framework:** FastAPI 0.115+
- **Server:** Uvicorn (ASGI)
- **Validation:** Pydantic 2.9+
- **Math/Simulation:** NumPy 1.24+
- **Real-time:** WebSockets 13+
- **Hosting:** Railway (Containerized Python)

---

## 🚀 Quick Start

### **Frontend**
```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-.git
cd ai-gpu-energy-optimizer-
npm install
npm run dev
# Open http://localhost:3000
```

### **Backend**
```bash
cd ai-engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API: http://localhost:8000
# WS:  ws://localhost:8000/ws
```

---

## 📡 API Reference

### **Endpoints**
| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Service health check |
| `GET`  | `/optimize` | Fetch current cluster metrics & AI recommendations |
| `POST` | `/optimize` | Submit custom GPU metrics for analysis |
| `WS`   | `/ws` | Real-time bidirectional data stream (2s intervals) |

### **Sample Response (`GET /optimize`)**
```json
{
  "timestamp": "2026-04-21T19:00:00Z",
  "clusters": [
    {
      "id": "h100-cluster-1",
      "name": "NVIDIA H100 Cluster",
      "location": "US-West",
      "gpu_utilization": 92.4,
      "temperature": 74.1,
      "power_draw": 1.82,
      "efficiency_score": 95.1
    }
  ],
  "total_power_mw": 3.06,
  "grid_carbon_intensity": 0.42,
  "recommendations": [
    {
      "action": "Shift 15% workload to off-peak",
      "estimated_savings_monthly": 18500,
      "priority": "high"
    }
  ]
}
```

---

## 📦 Deployment

### **Frontend (Vercel)**
1. Connect repository to Vercel
2. Set Environment Variables:
   - `NEXT_PUBLIC_API_URL` = Backend URL
   - `NEXT_PUBLIC_WS_URL` = WebSocket URL
3. Deploy (auto-builds on `main` push)

### **Backend (Railway)**
1. Create new project → Connect GitHub repo
2. **Root Directory:** `ai-engine`
3. Railway auto-detects `requirements.txt` & Python
4. Ensure `PORT` environment variable is set (default: `$PORT`)
5. Deploy & generate public domain

---

## 👤 Author & License

**Developed by:** Mike Bains  
**Contact:** [Mikebains41@gmail.com](mailto:Mikebains41@gmail.com)  
**GitHub:** [@mikebains41-debug](https://github.com/mikebains41-debug)

---

### 📄 License
**PROPRIETARY & CONFIDENTIAL**  
© 2026 Mike Bains. All Rights Reserved.  
Unauthorized reproduction, distribution, or modification of this software is strictly prohibited. For licensing inquiries, contact the author directly.

---

<div align="center">
  <strong>Built for performance. Optimized for sustainability.</strong><br>
  <sub>Deployed on Vercel + Railway • Powered by Next.js & FastAPI</sub>
</div>
