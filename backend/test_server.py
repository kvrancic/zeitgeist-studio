"""Test script to verify backend is working."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Zeitgeist Studio Backend\n")

# Test 1: Import config
print("1️⃣  Testing config import...")
try:
    from config import settings
    print(f"   ✅ Config loaded")
    print(f"   - Debug mode: {settings.debug}")
    print(f"   - API port: {settings.api_port}")
    print(f"   - Upload dir: {settings.upload_dir}")
except Exception as e:
    print(f"   ❌ Config failed: {e}")
    sys.exit(1)

# Test 2: Import agents
print("\n2️⃣  Testing agent imports...")
try:
    from agents.philosopher import ZeitgeistPhilosopher
    from agents.architect import CynicalContentArchitect
    from agents.optimizer import BrutalistOptimizer
    print("   ✅ All agents imported")
except Exception as e:
    print(f"   ❌ Agent import failed: {e}")
    sys.exit(1)

# Test 3: Import tasks and crew
print("\n3️⃣  Testing tasks and crew imports...")
try:
    from tasks.marketing_tasks import MarketingTasks
    from services.crew_service import MarketingCrew
    print("   ✅ Tasks and crew imported")
except Exception as e:
    print(f"   ❌ Tasks/crew import failed: {e}")
    sys.exit(1)

# Test 4: Import API routes
print("\n4️⃣  Testing API route imports...")
try:
    from api.routes import health, profile, trends, campaign, export
    print("   ✅ All API routes imported")
except Exception as e:
    print(f"   ❌ API routes import failed: {e}")
    sys.exit(1)

# Test 5: Import main app
print("\n5️⃣  Testing FastAPI app import...")
try:
    from main import app
    print("   ✅ FastAPI app loaded")
    print(f"   - App title: {app.title}")
    print(f"   - Routes: {len(app.routes)} registered")
except Exception as e:
    print(f"   ❌ App import failed: {e}")
    sys.exit(1)

# Test 6: List all routes
print("\n6️⃣  Registered API endpoints:")
from main import app
routes = [route for route in app.routes if hasattr(route, 'path')]
for route in sorted(routes, key=lambda r: r.path):
    methods = getattr(route, 'methods', ['GET'])
    print(f"   - {', '.join(methods):10} {route.path}")

print("\n" + "="*60)
print("✅ All tests passed! Backend is ready.")
print("="*60)
print("\n📝 Next steps:")
print("   1. Add real API keys to .env file")
print("   2. Start server: uvicorn main:app --reload --port 8000")
print("   3. Visit http://localhost:8000/docs for API documentation")
print("   4. Test health endpoint: curl http://localhost:8000/api/health")
