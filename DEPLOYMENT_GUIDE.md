# KPI Dashboard Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Streamlit Community Cloud (FREE)

**Best for:** Demos, portfolios, public applications

**Steps:**
1. Push your code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repository and branch
5. Set the main file path: `app.py`
6. Add environment variables:
   - `OPENROUTER_API_KEY` (for AI features)
   - `WHATSAPP_TOKEN` (optional)
   - `SLACK_TOKEN` (optional)
7. Click "Deploy"

**URL:** Your app will be available at `https://your-username-kpi-dashboard-streamlit-app-abcdef.streamlit.app/`

### Option 2: Railway ($5/month)

**Best for:** Production applications, private deployments

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up and connect GitHub
3. Click "Deploy from GitHub repo"
4. Select your KPI dashboard repository
5. Railway auto-detects Streamlit and deploys
6. Add environment variables in Railway dashboard
7. Get your custom URL

**Features:**
- Custom domains
- Automatic scaling
- Usage-based pricing
- Private applications

### Option 3: Render ($19/month)

**Best for:** Business applications, reliable hosting

**Steps:**
1. Go to [render.com](https://render.com)
2. Connect GitHub account
3. Create new "Web Service"
4. Select your repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Set environment variables
7. Deploy

### Option 4: Replit Deployments (Current)

**Steps:**
1. Click "Deploy" button in your Replit project
2. Configure your deployment settings
3. Set environment variables
4. Choose deployment type (Reserved VM recommended)
5. Launch deployment

## 📋 Environment Variables Required

For any deployment platform, configure these environment variables:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
WHATSAPP_TOKEN=your_whatsapp_token_here (optional)
WHATSAPP_PHONE=your_whatsapp_phone_number (optional)
SLACK_TOKEN=your_slack_bot_token_here (optional)
SLACK_CHANNEL=#alerts (optional)
```

## 🔧 Platform-Specific Configuration

### Streamlit Community Cloud
- Create `.streamlit/config.toml` file:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

### Railway/Render
- Ensure your app binds to `0.0.0.0` and the provided PORT
- Configure build commands in platform settings

### Docker Deployment
- Use the provided `Dockerfile`
- Build: `docker build -t kpi-dashboard .`
- Run: `docker run -p 5000:5000 kpi-dashboard`

## 🌐 Custom Domain Setup

### Free Options:
- Use platform-provided subdomain
- GitHub Pages (for static sites only)

### Paid Options:
- Buy domain from Namecheap, GoDaddy, etc.
- Configure DNS to point to your deployment platform
- Most platforms support custom domains in paid plans

## 📊 Monitoring & Maintenance

### Application Monitoring:
- Check application logs in your hosting platform
- Monitor database size (SQLite has limits)
- Watch for API quota limits (OpenRouter, WhatsApp, Slack)

### Scaling Considerations:
- **Single User**: Current SQLite setup works fine
- **Multiple Users**: Consider PostgreSQL migration
- **High Traffic**: Add Redis caching layer

## 🔒 Security Best Practices

### Environment Variables:
- Never commit API keys to Git
- Use platform secret management
- Rotate keys regularly

### Database Security:
- Backup SQLite database regularly
- Consider encrypting sensitive data
- Implement user authentication for multi-user deployments

## 💡 Deployment Recommendations

### For Learning/Demo:
**Use Streamlit Community Cloud** - Free, easy, perfect for showcasing

### For Business/Production:
**Use Railway or Render** - Reliable, scalable, professional features

### For Enterprise:
**Use AWS/GCP/Azure** - Full control, enterprise features, compliance

## 🐛 Common Deployment Issues

### Port Binding Issues:
```python
# Ensure your app binds to 0.0.0.0, not localhost
port = int(os.environ.get("PORT", 5000))
st.run(host="0.0.0.0", port=port)
```

### Missing Dependencies:
- Ensure all required packages are listed in requirements.txt
- Use specific version numbers for stability

### Environment Variable Issues:
- Double-check variable names and values
- Test locally with same environment variables

### File Path Issues:
- Use relative paths, not absolute paths
- Ensure uploaded files are handled properly in cloud environment

## 📈 Performance Optimization

### For Better Performance:
- Enable Streamlit caching with `@st.cache_data`
- Optimize database queries
- Compress images and large files
- Use CDN for static assets

### For Cost Optimization:
- Monitor usage on paid platforms
- Implement auto-scaling policies
- Use appropriate instance sizes

## 🎯 Next Steps After Deployment

1. **Test all features** on the deployed application
2. **Set up monitoring** and alerts
3. **Configure backup** strategy for data
4. **Add user authentication** if needed for multi-user access
5. **Set up CI/CD** for automatic deployments
6. **Monitor costs** and optimize as needed

Your KPI dashboard is now ready for deployment to any of these platforms!