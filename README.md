```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel Edge)                   │
│  Next.js 14 • TypeScript • Tailwind CSS • Recharts          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Dashboard  │  │   Analytics  │  │  Components  │     │
│  │   (SSR/CSR)  │  │  (Charts)    │  │   (UI Kit)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │ WSS / HTTPS
┌──────────────────────────▼──────────────────────────────────┐
│                     BACKEND (Railway)                       │
│  FastAPI • Uvicorn • Pydantic • NumPy • WebSockets          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   REST API   │  │  WebSocket   │  │  Metrics &   │     │
│  │  Endpoints   │  │   Streamer   │  │  Simulator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

### **Frontend**
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS
- **State:** React Hooks
- **Charts:** Recharts
- **Icons:** Lucide React
- **Hosting:** Vercel

### **Backend**
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Validation:** Pydantic
- **Math:** NumPy
- **Real-time:** WebSockets
- **Hosting:** Railway

---

## 🚀 Quick Start

### **Frontend**
```bash
git clone https://github.com/mikebains41-debug/ai-gpu-energy-optimizer-.git
cd ai-gpu-energy-optimizer-
npm installnpm run dev
```

### **Backend**
```bash
cd ai-engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Reference

**Base URL:** `https://ai-gpu-energy-optimizer-production.up.railway.app`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/optimize` | Get metrics + recommendations |
| `POST` | `/optimize` | Submit GPU metrics |
| `WS` | `/ws` | Real-time stream (2s) |

---

## 📦 Deployment

**Frontend (Vercel):**
1. Connect repo to Vercel
2. Add env vars: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_WS_URL`
3. Deploy

**Backend (Railway):**
1. Connect repo to Railway
2. Set Root Directory: `ai-engine`
3. Deploy

---

## 👤 Author & License

**Developed by:** Mike Bains  
**Contact:** [Mikebains41@gmail.com](mailto:Mikebains41@gmail.com)  
**GitHub:** [@mikebains41-debug](https://github.com/mikebains41-debug)

**License:** PROPRIETARY & CONFIDENTIAL  
© 2026 Mike Bains. All Rights Reserved.

---
<div align="center">
  <strong>Built for performance. Optimized for sustainability.</strong><br>
  <sub>Deployed on Vercel + Railway • Powered by Next.js & FastAPI</sub>
</div>
