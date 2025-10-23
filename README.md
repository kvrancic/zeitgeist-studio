# 🎨 Zeitgeist Studio

> **AI Marketing Campaign Generator** - Transform trend analysis into complete, ready-to-deploy marketing campaigns in minutes, powered by multi-agent AI.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Agents-purple)](https://crewai.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)

---

## 🚀 Project Overview

**Zeitgeist Studio** is a B2B SaaS platform that generates complete marketing campaigns in under 10 minutes. Input your company profile and select a trend (or let our AI find one), and receive a professional campaign package including:

- 📄 **Campaign Narrative** (Strategic PDF)
- ✍️ **SEO Blog Post** (Markdown)
- 📱 **Social Media Content** (Twitter, Instagram, TikTok)
- 👕 **T-Shirt Design Concepts** (Visual descriptions)

### The Secret Sauce: Three AI Agents

Our multi-agent system is powered by three specialized AI personas that work together:

1. **🧐 Zeitgeist Philosopher** - Cultural analyst who deconstructs trends to find deep psychological drivers
2. **✍️ Cynical Content Architect** - Creative writer who transforms insights into viral content
3. **📊 Brutalist Optimizer** - Technical SEO specialist who ensures everything converts

---

## 🏗️ Architecture

```
zeitgeist-studio/
├── frontend/          # Next.js 14 (App Router) + TypeScript
│   ├── app/          # Pages & routing
│   ├── components/   # React components
│   └── lib/          # Utilities & API client
├── backend/           # FastAPI + Python
│   ├── api/          # REST endpoints
│   ├── agents/       # CrewAI agent definitions
│   ├── tasks/        # Agent tasks
│   └── services/     # Business logic
├── shared/            # Shared types & constants
└── docs/              # Documentation
```

**Tech Stack:**
- **Frontend**: Next.js 14, TypeScript, TailwindCSS, Zustand
- **Backend**: FastAPI, CrewAI, OpenRouter (LLMs), Serper (search)
- **Deployment**: Vercel (frontend) + Railway (backend)

---

## 🎯 Features

### Phase 1: MVP (Current)
- ✅ Company profile input with document upload (PDF/DOCX/TXT)
- ✅ AI-powered trend discovery (Serper API + Philosopher agent)
- ✅ Manual topic input
- ✅ Real-time campaign generation with streaming updates
- ✅ Professional PDF export
- ✅ ZIP download with all assets

### Phase 2: Video Generation (Future)
- 🔮 Node-based video storyboarding
- 🔮 Multi-model video generation (Sora, Runway, Kling)
- 🔮 Interactive canvas editor

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and Python 3.9+
- OpenRouter API key ([Get one](https://openrouter.ai))
- Serper API key ([Get one](https://serper.dev))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/karlovrancic/zeitgeist-studio.git
cd zeitgeist-studio
```

**2. Set up backend**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

**3. Set up frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with backend URL
```

**4. Run development servers**

Terminal 1 (Backend):
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

---

## 📖 Usage

### Basic Workflow
1. **Set up company profile** - Enter company info, upload brand guidelines
2. **Discover trends** - Let AI find trending topics or input your own
3. **Generate campaign** - Watch agents work in real-time
4. **Export assets** - Download PDF narrative, blog, social posts

---

## 🤖 Agent System

Our agents are built on CrewAI and powered by Google's Gemini 2.5 Pro via OpenRouter.

### Pipeline Flow
```
Philosopher (Trend Analysis)
    ↓
Architect (Content Creation)
    ↓
Optimizer (SEO/Conversion)
    ↓
Architect (Final Polish)
```

Each agent has a distinct personality and expertise, ensuring campaigns are both creative and data-driven.

---

## 🛠️ Development

### Backend API Endpoints
- `GET /api/health` - Health check
- `POST /api/profile/create` - Save company profile
- `POST /api/trends/search` - AI trend discovery
- `POST /api/trends/manual` - Manual topic input
- `POST /api/campaign/generate` - Generate campaign (SSE streaming)
- `POST /api/export/pdf` - Export narrative as PDF
- `POST /api/export/zip` - Download all assets

### Environment Variables

**Backend (.env)**
```env
OPENROUTER_API_KEY=your_openrouter_key
SERPER_API_KEY=your_serper_key
OPENROUTER_PRO_MODEL=google/gemini-2.5-pro
OPENROUTER_LITE_MODEL=google/gemini-2.5-flash-lite
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 Documentation

- [API Documentation](./docs/api.md)
- [Agent System Design](./docs/agents.md)
- [Deployment Guide](./docs/deployment.md)
- [Contributing Guidelines](./docs/contributing.md)

---

## 🎓 Background

This project was inspired by [digital-twin](https://github.com/karlovrancic/digital-twin), a multi-agent system built for MIT AI Studio. Zeitgeist Studio takes that foundation and transforms it into a production-ready B2B product.

**Built by**: Karlo Vrančić
**Contact**: karlovrancic@g.harvard.edu
**Institution**: Harvard/MIT MS Student

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

---

## 🙏 Acknowledgments

- **CrewAI** - Multi-agent framework
- **OpenRouter** - Unified LLM access
- **Serper** - Web search API
- **TeeWiz** - Real-world application context

---

**🚀 Ready to transform your marketing workflow? Let's build something amazing.**
