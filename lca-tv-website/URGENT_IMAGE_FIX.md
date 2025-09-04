# 🚨 URGENT: Image Display Fix for LCA TV Website

## Problem Identified
The images are not displaying because the Flask app was generating URLs with double `/lca/lca/static/` instead of `/lca/static/`. This was caused by a problematic custom `url_for` function.

## ✅ IMMEDIATE FIX APPLIED

### 1. Fixed Flask App Configuration
**Problem**: Custom `url_for` function was adding `/lca` prefix twice
**Solution**: Removed custom `url_for` function and used Flask's built-in URL generation

**Files Updated**:
- ✅ `app.py` - Fixed version created (removes double `/lca` issue)
- ✅ `app_fixed.py` - Clean version without URL duplication
- ✅ `app_backup.py` - Backup of original problematic version

### 2. Corrected Static File Configuration
**Before**: `static_url_path='/lca/static'` (causing double prefix)
**After**: `static_url_path='/static'` (correct for subdirectory deployment)

### 3. Enhanced .htaccess Configuration
**New file**: `.htaccess_fixed` - Proper static file handling for PlanetHoster

## 🚀 DEPLOYMENT STEPS (URGENT)

### Step 1: Upload Fixed Files
Replace these files on your server immediately:

1. **Replace `app.py`** with the fixed version
2. **Replace `.htaccess`** with `.htaccess_fixed`
3. **Restart the Python application** in cPanel

### Step 2: Verify Fix
After uploading, test these URLs:

1. **Homepage**: https://edifice.bf/lca/
2. **Logo direct**: https://edifice.bf/lca/static/images/LOGO%20LCA.png
3. **Debug page**: https://edifice.bf/lca/debug

### Step 3: Clear Cache
1. Visit: https://edifice.bf/lca/api/cache/clear (if logged in as admin)
2. Or restart the Python app in cPanel

## 📋 VERIFICATION CHECKLIST

After deployment, verify these work:
- [ ] Logo appears in header
- [ ] Slider images display correctly
- [ ] All navigation links work
- [ ] Static files load (CSS, JS)
- [ ] No broken image icons

## 🔧 Technical Details

### Root Cause
The original `app.py` had this problematic code:
```python
# PROBLEMATIC CODE (REMOVED)
def url_for(endpoint, **values):
    url = flask_url_for(endpoint, **values)
    if not url.startswith('/lca'):
        url = '/lca' + url  # This was adding /lca twice!
    return url
```

### Fixed Configuration
```python
# FIXED CODE
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['APPLICATION_ROOT'] = '/lca'
# No custom url_for function needed!
```

## 🆘 If Images Still Don't Show

### Quick Diagnostic Commands:
```bash
# Check if files exist
ls -la static/images/LOGO\ LCA.png

# Test direct access
curl -I https://edifice.bf/lca/static/images/LOGO\ LCA.png

# Check permissions
chmod 644 static/images/*
chmod 755 static/
```

### Emergency Fallback:
If the fix doesn't work immediately:

1. **Check Python app logs** in cPanel
2. **Restart the Python application**
3. **Verify file upload** completed successfully
4. **Test direct image URLs** in browser

## 📞 Support URLs

- **Health Check**: https://edifice.bf/lca/health
- **Debug Info**: https://edifice.bf/lca/debug
- **Direct Logo Test**: https://edifice.bf/lca/static/images/LOGO%20LCA.png

## ⚡ Expected Results

After applying this fix:
- ✅ Logo will display in header
- ✅ Slider images will show correctly
- ✅ All static files will load properly
- ✅ URLs will be `/lca/static/...` instead of `/lca/lca/static/...`

---

**PRIORITY**: CRITICAL - Deploy immediately to fix image display issues
**ESTIMATED FIX TIME**: 5-10 minutes
**IMPACT**: Resolves all image display problems on the live site