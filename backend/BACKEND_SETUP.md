# 🚀 Zeitgeist Studio Backend - Setup & Testing Guide

## ✅ Status: All Dependencies Installed & Tests Passing

The backend has been successfully set up and all import tests pass!

---

## 🔧 Quick Start

### 1. Your virtual environment is already created with all dependencies installed:
```bash
cd /Users/karlovrancic/Desktop/zeitgeist-studio/backend
source .venv/bin/activate
```

### 2. Add your real API keys to `.env`:

Open `.env` file and replace the dummy keys:
```bash
OPENROUTER_API_KEY=sk-or-v1-YOUR-REAL-KEY-HERE
SERPER_API_KEY=YOUR-REAL-SERPER-KEY-HERE
```

Get your keys here:
- **OpenRouter**: https://openrouter.ai/keys
- **Serper**: https://serper.dev/api-key

### 3. Start the server:

**Option A: Use the start script (recommended)**
```bash
./start_server.sh
```

**Option B: Manual start**
```bash
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Test the API:

Visit these URLs in your browser:
- **Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/api/health
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **API Schema**: http://localhost:8000/redoc (ReDoc)

Or use curl:
```bash
curl http://localhost:8000/api/health
```

---

## 📊 What's Working

### ✅ All Backend Components:
1. **FastAPI Server** - Main application with CORS configured
2. **Configuration** - Settings loaded from .env
3. **Agents** - All 3 agents (Philosopher, Architect, Optimizer)
4. **Tasks** - Marketing tasks system
5. **Crew Service** - Multi-agent orchestration
6. **API Routes** - All 5 endpoint groups:
   - `/api/health` - Health checks
   - `/api/profile` - Company profile management
   - `/api/trends` - Trend discovery
   - `/api/campaign` - Campaign generation (SSE streaming)
   - `/api/export` - PDF/ZIP export

### 📋 Test Results:
```
✅ Config loaded
✅ All agents imported (Philosopher, Architect, Optimizer)
✅ Tasks and crew imported
✅ All API routes imported
✅ FastAPI app loaded with 16 registered routes
```

---

## 🏗️ What's Implemented (Skeletons)

The API endpoints exist and return mock data. **You or I will need to wire up the actual agent logic:**

### 1. Trend Search (`/api/trends/search`)
- ✅ Endpoint structure exists
- ✅ Pydantic models defined
- ⏳ TODO: Wire up Philosopher agent with Serper API

### 2. Campaign Generation (`/api/campaign/generate`)
- ✅ SSE streaming structure exists
- ✅ Real-time progress updates framework
- ⏳ TODO: Wire up full 4-step crew pipeline

### 3. File Upload (`/api/profile/create`)
- ✅ Multipart form data handling
- ✅ File validation
- ⏳ TODO: PDF/DOCX text extraction + LLM summarization

### 4. PDF/ZIP Export (`/api/export/...`)
- ✅ Endpoint structure
- ⏳ TODO: ReportLab PDF generation
- ⏳ TODO: ZIP file assembly

---

## 🐛 Dependency Issues Fixed

All dependency conflicts have been resolved:

1. ✅ **openai version** - Updated to `>=1.13.3,<2.0.0`
2. ✅ **pydantic version** - Updated to `>=2.6.1,<3.0.0`
3. ✅ **crewai version** - Upgraded to `1.1.0` (matches digital-twin)
4. ✅ **setuptools** - Added for pkg_resources
5. ✅ **CORS config** - Fixed parsing from string to list

---

## 📝 Next Steps

### For Complete MVP:

1. **Wire up Philosopher agent** in `/api/routes/trends.py`:
   ```python
   crew = MarketingCrew(use_lite=False)
   result = crew.quick_analysis(f"Find trending topics for {request.company_name}")
   ```

2. **Wire up full campaign pipeline** in `/api/routes/campaign.py`:
   ```python
   crew = MarketingCrew(use_lite=False)
   result = crew.analyze_trend(request.trend_name)
   ```

3. **Implement PDF generation** using ReportLab

4. **Implement document extraction** for uploaded files

5. **Build frontend** (Task #6 in todo list)

---

## 🚨 Important Notes

- **Dummy API keys are in `.env`** - Replace with real ones before testing agent functionality
- **Agents won't work without real API keys** - OpenRouter and Serper are required
- **Mock data is returned** for now - endpoints work but use placeholder responses
- **All imports pass** - The structure is solid, just needs logic wiring

---

## 🆘 Troubleshooting

### Server won't start?
```bash
cd /Users/karlovrancic/Desktop/zeitgeist-studio/backend
source .venv/bin/activate
python test_server.py  # Run diagnostic tests
```

### Import errors?
```bash
pip install -r requirements.txt  # Reinstall dependencies
```

### Port already in use?
```bash
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
```

---

## ✨ You're Ready!

The backend foundation is complete and tested. All that's left is:
1. Add real API keys
2. Wire up the TODOs in the route handlers
3. Build the frontend (Next.js)

**Great work so far! 🎉**
