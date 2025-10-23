# 🎯 Zeitgeist Studio - Project Status

**Last Updated**: October 22, 2025
**Current Phase**: Backend Complete, Starting Frontend
**Overall Progress**: ~25% (5/21 tasks complete)

---

## 📋 Implementation Plan Overview

We're building **Zeitgeist Studio** - a B2B Marketing Campaign Generator MVP with:
- **Backend**: FastAPI + CrewAI agents (from digital-twin)
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Deployment**: Vercel (frontend) + Railway (backend)
- **Goal**: Full PRD MVP with real-time streaming, PDF/ZIP export, AI trend search

### Key Features:
1. Company profile input with document upload (PDF/DOCX extraction)
2. AI-powered trend discovery (Serper API + Philosopher agent)
3. Manual topic input option
4. 4-step campaign generation with real-time streaming (SSE)
5. Professional exports (PDF narrative, ZIP with all assets)

---

## ✅ Completed Tasks (5/21)

### Phase 1: Backend Infrastructure ✅
1. ✅ Created new zeitgeist-studio repository structure
2. ✅ Set up backend directory with FastAPI scaffolding
3. ✅ Copied agents from digital-twin (philosopher, architect, optimizer)
4. ✅ Copied tasks and crew orchestration from digital-twin
5. ✅ Set up FastAPI endpoints structure (health, profile, trends, campaign, export)

**Git Status**: 7 commits, clean working tree
**Backend Location**: `/Users/karlovrancic/Desktop/zeitgeist-studio/backend/`

---

## 🚧 In Progress / Next Steps (16 remaining)

### Phase 2: Frontend Setup (Next 2 tasks)
6. ⏳ **NEXT**: Set up Next.js 14 frontend with TypeScript and TailwindCSS
7. ⏳ Create frontend folder structure (app, components, lib)

### Phase 3: Company Profile System (2 tasks)
8. ⏳ Implement backend profile management endpoints with file upload
9. ⏳ Build CompanyProfileForm component with validation

### Phase 4: Trend Identification (3 tasks)
10. ⏳ Implement AI trend search endpoint with Philosopher agent
11. ⏳ Implement manual trend input endpoint
12. ⏳ Build TrendSelector component with AI/manual toggle

### Phase 5: Campaign Generation (2 tasks)
13. ⏳ Implement SSE streaming campaign generation endpoint
14. ⏳ Build CampaignGenerator with real-time pipeline progress

### Phase 6: Export System (3 tasks)
15. ⏳ Implement PDF export endpoint with ReportLab
16. ⏳ Implement ZIP export endpoint with all assets
17. ⏳ Add download functionality to frontend

### Phase 7: Polish & Deployment (4 tasks)
18. ⏳ Polish UI/UX with loading states and error handling
19. ⏳ Set up Vercel deployment for frontend
20. ⏳ Set up Railway deployment for backend
21. ⏳ End-to-end testing and demo preparation

---

## 🏗️ Current Architecture

### Backend Structure (Complete)
```
backend/
├── main.py              ✅ FastAPI app with all routers included
├── config.py            ✅ Settings management with pydantic
├── requirements.txt     ✅ All dependencies (fixed openai version)
├── agents/
│   ├── philosopher.py   ✅ Zeitgeist Philosopher (with SerperDevTool)
│   ├── architect.py     ✅ Cynical Content Architect
│   └── optimizer.py     ✅ Brutalist Optimizer
├── tasks/
│   └── marketing_tasks.py  ✅ All agent task definitions
├── services/
│   └── crew_service.py  ✅ MarketingCrew orchestration
└── api/routes/
    ├── health.py        ✅ Health checks
    ├── profile.py       ✅ Company profile + file upload (skeleton)
    ├── trends.py        ✅ AI search + manual input (skeleton)
    ├── campaign.py      ✅ SSE streaming generation (skeleton)
    └── export.py        ✅ PDF + ZIP export (skeleton)
```

**Status**: All routes have Pydantic models and endpoint structure. Need to wire up actual agent logic.

### Frontend Structure (Not Started)
```
frontend/
├── app/                 ⏳ Next.js App Router pages
├── components/          ⏳ React components
└── lib/                 ⏳ API client, utilities, state
```

---

## 🔑 Important Context for Next Session

### 1. Agent Behavior - CRITICAL
**DO NOT MODIFY AGENT PERSONALITIES OR CORE LOGIC**. The three agents are:
- **Philosopher**: Sarcastic, finds deep psychological truths in trends
- **Architect**: Cynical, weaponizes language for engagement
- **Optimizer**: Brutalist, models humans as state machines

These work perfectly in the original `digital-twin` project. Keep them intact.

### 2. What Needs Implementation (Skeletons Already Built)

The API routes exist but return mock data. Need to wire up:

**Trend Search** (`backend/api/routes/trends.py:36`):
```python
# TODO: Implement actual trend search with Philosopher
# crew = MarketingCrew(use_lite=False)
# result = crew.quick_analysis(request.company_description)
```

**Campaign Generation** (`backend/api/routes/campaign.py:50`):
```python
# TODO: Actually run full pipeline
# crew = MarketingCrew(use_lite=False)
# result = crew.analyze_trend(request.trend_name)
```

**PDF Export** (`backend/api/routes/export.py:39`):
```python
# TODO: Implement actual PDF generation with ReportLab
```

**File Upload** (`backend/api/routes/profile.py:56`):
```python
# TODO: Implement document extraction (PDF, DOCX, TXT)
# Use pypdf2, python-docx, then summarize with LLM if >2000 tokens
```

### 3. Design Decisions Made

- **Tech Stack**: Next.js 14 (App Router) + TypeScript + FastAPI
- **Streaming**: SSE (Server-Sent Events) for real-time pipeline updates
- **Storage**: localStorage for MVP (no database)
- **Models**: Gemini 2.5 Pro (complex) + Flash (simple) via OpenRouter
- **Deployment**: Vercel + Railway (configured from start)

### 4. User Preferences

From planning session:
- ✅ Full PRD MVP (all features)
- ✅ Text-only (no voice capabilities)
- ✅ Flexible tech stack (optimized for speed)
- ✅ Flexible timeline (quality over rush)
- ✅ New separate repository
- ✅ Real-time pipeline updates (streaming UX)
- ✅ TypeScript for frontend
- ✅ Plan for deployment from start

---

## 🚀 How to Continue This Project

### For Karlo (or Future AI Assistant):

1. **Load this document** to understand current state
2. **Check the todo list** (items 6-21 are pending)
3. **Reference the plan** in the original chat or in README.md
4. **Key principle**: Never assume, always ask Karlo before:
   - Changing agent personalities or core logic
   - Adding features not in the PRD
   - Making architectural decisions
   - Implementing summarization/extraction logic

### Commands to Get Started:

```bash
# 1. Navigate to project
cd /Users/karlovrancic/Desktop/zeitgeist-studio

# 2. Set up backend (if not done)
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys

# 3. Test backend
uvicorn main:app --reload --port 8000
# Visit http://localhost:8000/docs

# 4. Set up frontend (next step)
cd ../frontend
# (Frontend setup is task #6 - not started yet)
```

---

## 🐛 Known Issues / Fixes Applied

1. ✅ **FIXED**: Dependency conflict between `openai==1.3.5` and `crewai==0.28.8`
   - Solution: Changed to `openai>=1.13.3,<2.0.0` in requirements.txt
   - Commit: `2dc456f`

---

## 📝 Critical Checkpoints (Where to Ask Karlo)

Based on original plan, I MUST ask Karlo before:

1. ❓ Before implementing document summarization logic - ask about token limits
2. ❓ After building trend selector UI - show mockup for approval
3. ❓ Before finalizing PDF export format - ask about branding/layout
4. ❓ After backend is deployed - ask Karlo to test API keys
5. ❓ Before going live - full demo walkthrough for approval

---

## 📚 Reference Documents

- **Full Implementation Plan**: See original chat or README.md
- **Original Project** (digital-twin): `/Users/karlovrancic/Desktop/digital-twin/`
- **Proposal**: `/Users/karlovrancic/Desktop/digital-twin/new-project-guide/proposal.tex`
- **PRD**: `/Users/karlovrancic/Desktop/digital-twin/new-project-guide/PRD.md` (38k tokens, prefer proposal)

---

## 🎯 Next Immediate Steps

**Task #6**: Set up Next.js 14 frontend with TypeScript and TailwindCSS

```bash
cd /Users/karlovrancic/Desktop/zeitgeist-studio/frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

Then configure:
- TailwindCSS
- Shadcn/UI components
- Zustand for state management
- Axios for API calls
- Basic folder structure (app/, components/, lib/)

**Estimated Time**: 1-2 hours
**Deliverable**: Working Next.js dev server with TypeScript + Tailwind

---

**Last Git Commit**: `2dc456f` - Fix dependency conflict
**Branch**: `master`
**Working Directory**: Clean
