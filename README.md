# 🤖 AI GPU Energy Optimizer

[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com)
[![Backend](https://img.shields.io/badge/Backend-Railway-purple?style=for-the-badge&logo=railway)](https://railway.app)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

> Real-time GPU monitoring & AI-driven energy optimization platform with WebSocket streaming.

---

## ✨ Features

- 📊 **Live GPU Metrics** - Utilization, temperature, power draw
- 🧠 **AI Optimization** - Automated recommendations
- 💰 **Cost Analytics** - ROI tracking & savings projections
- 🌍 **Sustainability** - CO₂ reduction & renewable energy tracking
- 🔔 **Smart Alerts** - Threshold-based notifications
- 📱 **Mobile-First** - Responsive dark mode UI

---

## 🌐 Live Demo

**Frontend:** [https://vb9gyxmx-mikebains41gmailcom.vercel.app](https://vb9gyxmx-mikebains41gmailcom.vercel.app)  
**Backend API:** [https://ai-gpu-energy-optimizer-production.up.railway.app](https://ai-gpu-energy-optimizer-production.up.railway.app)

---

## 🛠 Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS, Recharts  
**Backend:** FastAPI, Python, NumPy, WebSockets  
**Hosting:** Vercel + Railway

---

## 🚀 Quick Start

**Frontend:**
```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-.git
cd ai-gpu-energy-optimizer-
npm install && npm run dev
```

**Backend:**
```bash
cd ai-engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/optimize` | Get metrics & recommendations |
| POST | `/optimize` | Submit GPU metrics |
| WS | `/ws` | Real-time stream |

---

## 📦 Deployment

**Vercel (Frontend):**
1. Connect repo
2. Add env vars: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_WS_URL`
3. Deploy

**Railway (Backend):**
1. Connect repo
2. Set Root Directory: `ai-engine`
3. Deploy

---

## 👤 Author

**Mike Bains**  
📧 Mikebains41@gmail.com  
🔗 [@mikebains41-debug](https://github.com/mikebains41-debug)

---

**License:** PROPRIETARY © 2026 Mike Bains. All Rights Reserved.

<div align="center">
  <sub>Built with ❤️ on Vercel + Railway</sub>
</div>
