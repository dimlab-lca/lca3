# LCA TV - Production Deployment Guide

## 🚀 Ready for Hosting - Complete Setup

Your LCA TV website is now **production-ready** and optimized for PlanetHoster hosting with dual domain access.

### 📋 Pre-Deployment Checklist

#### ✅ Files Ready for Upload
- [x] `app_production_ready.py` - Main production application
- [x] `passenger_wsgi_production.py` - Production WSGI entry point
- [x] `run_production.py` - Production run script
- [x] `requirements_production.txt` - Optimized dependencies
- [x] `.env_production` - Environment configuration template
- [x] All templates with beautiful slider using your images
- [x] Static files (CSS, JS, images) properly organized
- [x] Error pages (404.html, 500.html) with correct URLs

#### ✅ Production Features
- [x] **Performance Optimized**: Aggressive caching, reduced API calls
- [x] **Error Handling**: Comprehensive error handling and logging
- [x] **Security**: Production-safe configuration, secure sessions
- [x] **Subdirectory Support**: Works with edifice.bf/lca
- [x] **Fallback System**: Graceful degradation if APIs fail
- [x] **Mobile Responsive**: Perfect on all devices
- [x] **SEO Optimized**: Proper meta tags and structure

### 🌐 Domain Configuration

#### Primary Access
- **URL**: `https://edifice.bf/lca`
- **Method**: Subdirectory deployment

#### Secondary Access  
- **URL**: `https://tv-lca.edifice.bf`
- **Method**: Subdomain (if configured)

### 📁 File Upload Structure

Upload these files to your PlanetHoster hosting:

```
/public_html/lca/
├── app_production_ready.py          # Main application
├── passenger_wsgi.py                # WSGI entry (rename from passenger_wsgi_production.py)
├── run.py                          # Run script (rename from run_production.py)
├── requirements.txt                # Dependencies (rename from requirements_production.txt)
├── .env                           # Environment config (copy from .env_production)
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│       ├── LOGO LCA.png
│       ├── FRANC PARLER (TOUS LES MERCREDIS A 20H 40).png
│       ├── 7 AFRIQUE (TOUS LES DIMANCHES A 13H 00).png
│       ├── QUESTIONS DE FEMMES (TOUS LES LUNDIS A 20H 40).png
│       ├── SOLEIL D_AFRIQUE (DU LUNDI AU VENDREDI A 11H 00).png
│       └── ... (other images)
└── templates/
    ├── base.html
    ├── home.html
    ├── live.html
    ├── videos.html
    ├── journal.html
    ├── emissions.html
    ├── publicite.html
    ├── about.html
    ├── contact.html
    ├── login.html
    ├── dashboard.html
    ├── 404.html
    └── 500.html
```

### 🔧 Deployment Steps

#### 1. Upload Files
```bash
# Upload all files to /public_html/lca/ directory
# Ensure proper file permissions:
# - Directories: 755
# - Python files: 644
# - Static files: 644
```

#### 2. Rename Production Files
```bash
# In your hosting file manager or via SSH:
mv passenger_wsgi_production.py passenger_wsgi.py
mv run_production.py run.py
mv requirements_production.txt requirements.txt
cp .env_production .env
```

#### 3. Configure Environment Variables
Edit `.env` file with your actual values:
```bash
# CRITICAL: Change these values
SECRET_KEY=your-super-secret-production-key-here
ADMIN_PASSWORD=your-secure-admin-password
MUSK_PASSWORD=your-secure-musk-password
EDITOR_PASSWORD=your-secure-editor-password

# Optional: Add your YouTube API key for real videos
YOUTUBE_API_KEY=your-youtube-api-key-here
YOUTUBE_CHANNEL_ID=your-channel-id-here
```

#### 4. Install Dependencies
In PlanetHoster cPanel Python app manager:
```bash
pip install -r requirements.txt
```

#### 5. Set Python Version
- Ensure Python 3.9 is selected in cPanel
- Set entry point to `passenger_wsgi.py`

#### 6. Configure Domain/Subdirectory
- Main domain: Point `/lca` to the application directory
- Subdomain: Create `tv-lca.edifice.bf` pointing to same directory

### 🎯 Features Included

#### 🎨 Beautiful Homepage
- **Professional slider** with your actual program banners
- **Auto-advancing slides** every 5 seconds
- **Touch/swipe support** for mobile
- **Responsive design** for all devices

#### 📺 Content Management
- **YouTube integration** with fallback videos
- **Category filtering** (Actualités, Débats, Culture, Sport, etc.)
- **Live streaming** page with embedded player
- **Program schedule** display

#### 🔐 Admin Dashboard
- **Secure login** system
- **Content management** interface
- **Cache management** tools
- **System monitoring** capabilities

#### 📱 Mobile Optimization
- **Mobile-first design**
- **Touch-friendly** navigation
- **Optimized images** and loading
- **Progressive enhancement**

### 🛠 Admin Access

#### Login Credentials
- **URL**: `https://edifice.bf/lca/login`
- **Username**: `admin` | **Password**: (set in .env)
- **Username**: `musk` | **Password**: (set in .env)
- **Username**: `editor` | **Password**: (set in .env)

#### Dashboard Features
- View all videos and content
- Clear cache for updates
- Monitor system health
- Manage publicity spaces

### 🔍 Testing URLs

After deployment, test these URLs:

#### Main Pages
- `https://edifice.bf/lca/` - Homepage
- `https://edifice.bf/lca/live` - Live streaming
- `https://edifice.bf/lca/videos` - All videos
- `https://edifice.bf/lca/journal` - News/Journal
- `https://edifice.bf/lca/emissions` - Programs
- `https://edifice.bf/lca/about` - About page
- `https://edifice.bf/lca/publicite` - Advertising

#### Admin & API
- `https://edifice.bf/lca/login` - Admin login
- `https://edifice.bf/lca/dashboard` - Admin dashboard
- `https://edifice.bf/lca/health` - Health check
- `https://edifice.bf/lca/api/videos` - Videos API

### 🚨 Troubleshooting

#### Common Issues & Solutions

1. **500 Internal Server Error**
   - Check file permissions (755 for directories, 644 for files)
   - Verify Python 3.9 is selected
   - Check error logs in cPanel

2. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path configuration

3. **Static Files Not Loading**
   - Verify static files are in `/static/` directory
   - Check file permissions
   - Clear browser cache

4. **Subdirectory URLs Not Working**
   - Verify APPLICATION_ROOT is set to '/lca'
   - Check .htaccess configuration if needed

#### Debug Endpoints
- `https://edifice.bf/lca/debug` - System information
- `https://edifice.bf/lca/health` - Health status

### 📊 Performance Features

#### Caching System
- **Aggressive caching** for API responses
- **TTL-based expiration** (5-10 minutes)
- **Memory management** to prevent issues
- **Admin cache clearing** capability

#### Optimization
- **Reduced API calls** for better performance
- **Fallback content** when APIs are unavailable
- **Compressed responses** and optimized images
- **Lazy loading** for better user experience

### 🔒 Security Features

#### Production Security
- **Secure session management**
- **CSRF protection** built-in
- **Environment variable** configuration
- **Error handling** without information disclosure
- **Admin authentication** required for sensitive areas

### 📈 Monitoring

#### Health Checks
- **System status**: `/health` endpoint
- **Performance monitoring** built-in
- **Error logging** for troubleshooting
- **Cache statistics** available

### 🎉 Launch Checklist

Before going live:

- [ ] Upload all files to `/public_html/lca/`
- [ ] Rename production files correctly
- [ ] Configure `.env` with secure passwords
- [ ] Install dependencies via cPanel
- [ ] Test all main pages
- [ ] Test admin login and dashboard
- [ ] Verify mobile responsiveness
- [ ] Check error pages (404, 500)
- [ ] Test API endpoints
- [ ] Clear any test data

### 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review PlanetHoster documentation
3. Check application logs in cPanel
4. Use debug endpoints for system information

---

## 🎊 Your LCA TV website is ready for production!

**Access URLs:**
- **Primary**: https://edifice.bf/lca
- **Subdomain**: https://tv-lca.edifice.bf (if configured)

**Features:**
✅ Beautiful slider with your program banners  
✅ Professional responsive design  
✅ Admin dashboard with content management  
✅ YouTube integration with fallbacks  
✅ Mobile-optimized experience  
✅ Production-ready performance  
✅ Comprehensive error handling  
✅ Security best practices  

Your website showcases LCA TV professionally with all the features needed for a successful television station website! 🚀📺