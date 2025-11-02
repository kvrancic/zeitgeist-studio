# 🚀 Deployment Guide

This guide walks you through deploying Zeitgeist Studio to production using Vercel (frontend) and Railway (backend).

---

## 📋 Prerequisites

Before deploying, ensure you have:

1. **API Keys**
   - [OpenRouter API Key](https://openrouter.ai) - For LLM access (Gemini 2.5 Pro)
   - [Serper API Key](https://serper.dev) - For trend search

2. **Accounts**
   - [Vercel Account](https://vercel.com) - For frontend hosting
   - [Railway Account](https://railway.app) - For backend hosting

3. **Git Repository**
   - Push this project to GitHub (or GitLab/Bitbucket)

---

## 🔧 Backend Deployment (Railway)

### Step 1: Create Railway Project

1. Go to [Railway](https://railway.app) and create a new project
2. Select **"Deploy from GitHub repo"**
3. Choose this repository
4. Railway will automatically detect the Dockerfile

### Step 2: Configure Environment Variables

In Railway project settings, add these environment variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
SERPER_API_KEY=your_serper_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_PRO_MODEL=google/gemini-2.5-pro
OPENROUTER_LITE_MODEL=google/gemini-2.5-flash-lite
API_HOST=0.0.0.0
API_PORT=$PORT
DEBUG=False
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
MAX_UPLOAD_SIZE_MB=5
CREW_VERBOSE=False
MAX_RPM=30
```

**Important Notes:**
- Railway automatically provides `$PORT` - don't hardcode it
- Update `ALLOWED_ORIGINS` after deploying frontend (Step 3)
- Set `DEBUG=False` for production

### Step 3: Deploy

1. Railway will automatically deploy when you push to main branch
2. Copy your Railway URL (e.g., `https://zeitgeist-backend.up.railway.app`)
3. Test the health endpoint: `https://your-railway-url.up.railway.app/api/health`

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Import Project to Vercel

1. Go to [Vercel](https://vercel.com) and click **"Add New Project"**
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `./` (project root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/.next`
   - **Install Command**: `cd frontend && npm install`

### Step 2: Configure Environment Variables

Add this environment variable in Vercel project settings:

```env
NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app
```

Replace `your-railway-url` with your actual Railway deployment URL from Step 3 above.

### Step 3: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. Copy your Vercel URL (e.g., `https://zeitgeist-studio.vercel.app`)

### Step 4: Update Backend CORS

Go back to Railway and update the `ALLOWED_ORIGINS` environment variable:

```env
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

This allows your frontend to communicate with the backend.

---

## ✅ Verification

### Test Backend Health

```bash
curl https://your-railway-url.up.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-..."
}
```

### Test Frontend

1. Visit your Vercel URL
2. Create a company profile
3. Search for trends (tests Serper API)
4. Generate a campaign (tests OpenRouter API)

---

## 🔄 Continuous Deployment

Both Vercel and Railway support automatic deployments:

- **Push to main branch** → Automatic deployment
- **Pull requests** → Preview deployments (Vercel only)

---

## 📊 Monitoring & Logs

### Railway Logs

1. Go to Railway dashboard
2. Select your project
3. Click **"Logs"** to view real-time logs
4. Monitor API requests and agent workflows

### Vercel Logs

1. Go to Vercel dashboard
2. Select your project
3. Click **"Logs"** to view function logs
4. Monitor build and runtime errors

---

## 🐛 Troubleshooting

### Build Fails

**Frontend Build Error**
```bash
# Run locally to debug
cd frontend
npm run build
```

**Backend Build Error**
- Check Railway logs for Docker build errors
- Ensure `requirements.txt` includes all dependencies
- Verify Python version (3.11)

### Runtime Errors

**CORS Errors**
- Verify `ALLOWED_ORIGINS` in Railway includes your Vercel URL
- Check that URLs use `https://` (not `http://`)

**API Key Errors**
- Verify environment variables are set in Railway
- Check OpenRouter dashboard for API key validity
- Ensure Serper API key has remaining credits

**500 Internal Server Error**
- Check Railway logs for Python tracebacks
- Verify all environment variables are set correctly
- Test API endpoints locally first

---

## 💰 Cost Estimation

### Railway (Backend)
- **Starter Plan**: $5/month (500 hours)
- **Pro Plan**: $20/month (unlimited hours)
- Recommended: Start with Starter plan

### Vercel (Frontend)
- **Hobby**: Free (for personal projects)
- **Pro**: $20/month (for commercial use)
- Recommended: Hobby plan for MVP

### API Costs
- **OpenRouter**: Pay per token (~$0.01-0.05 per campaign)
- **Serper**: Free tier (2,500 searches), then $50/month
- Estimated: ~$10-50/month depending on usage

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** - They're already in `.gitignore`
2. **Use environment variables** for all secrets
3. **Enable HTTPS only** in production
4. **Rotate API keys** regularly
5. **Set up monitoring** for suspicious activity
6. **Use rate limiting** to prevent abuse

---

## 🚀 Next Steps

After successful deployment:

1. **Custom Domain**: Add your domain in Vercel settings
2. **Analytics**: Set up Vercel Analytics
3. **Error Tracking**: Integrate Sentry for error monitoring
4. **Database**: Add PostgreSQL for user data (future)
5. **Auth**: Implement authentication (future)

---

## 📞 Support

If you encounter issues:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review Railway and Vercel logs
3. Test locally first: `npm run dev` (frontend) and `uvicorn main:app --reload` (backend)
4. Open an issue on GitHub

---

**Deployment complete! 🎉**

Your Zeitgeist Studio is now live and ready to generate amazing marketing campaigns.
