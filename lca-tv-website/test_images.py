#!/usr/bin/env python3
"""
Image Verification Script for LCA TV Website
Run this script to check if all required images exist
"""

import os
from pathlib import Path

def check_images():
    """Check if all required images exist"""
    
    # Define required images
    required_images = [
        'LOGO LCA.png',
        'FRANC PARLER (TOUS LES MERCREDIS A 20H 40).png',
        '7 AFRIQUE (TOUS LES DIMANCHES A 13H 00).png',
        'QUESTIONS DE FEMMES (TOUS LES LUNDIS A 20H 40).png',
        'SOLEIL D_AFRIQUE (DU LUNDI AU VENDREDI A 11H 00).png'
    ]
    
    # Check static/images directory
    images_dir = Path('static/images')
    
    print("🔍 LCA TV Image Verification")
    print("=" * 50)
    
    if not images_dir.exists():
        print("❌ ERROR: static/images directory not found!")
        return False
    
    print(f"📁 Checking directory: {images_dir.absolute()}")
    print()
    
    all_found = True
    
    for image in required_images:
        image_path = images_dir / image
        if image_path.exists():
            size = image_path.stat().st_size
            print(f"✅ {image} - {size:,} bytes")
        else:
            print(f"❌ {image} - NOT FOUND")
            all_found = False
    
    print()
    print("📋 All files in static/images:")
    print("-" * 30)
    
    try:
        for file in sorted(images_dir.iterdir()):
            if file.is_file() and not file.name.startswith('.'):
                size = file.stat().st_size
                print(f"   {file.name} - {size:,} bytes")
    except Exception as e:
        print(f"Error listing files: {e}")
    
    print()
    if all_found:
        print("🎉 SUCCESS: All required images found!")
        print("✅ Your images should display correctly when deployed.")
    else:
        print("⚠️  WARNING: Some required images are missing!")
        print("❗ Upload missing images to fix display issues.")
    
    return all_found

def check_permissions():
    """Check file permissions (Unix/Linux only)"""
    try:
        images_dir = Path('static/images')
        if not images_dir.exists():
            return
        
        print()
        print("🔐 File Permissions Check:")
        print("-" * 30)
        
        for file in images_dir.iterdir():
            if file.is_file():
                perms = oct(file.stat().st_mode)[-3:]
                print(f"   {file.name}: {perms}")
                
                if perms != '644':
                    print(f"   ⚠️  Recommended: chmod 644 {file}")
        
    except Exception as e:
        print(f"Permission check not available: {e}")

def generate_test_html():
    """Generate a test HTML file to verify images"""
    
    required_images = [
        'LOGO LCA.png',
        'FRANC PARLER (TOUS LES MERCREDIS A 20H 40).png',
        '7 AFRIQUE (TOUS LES DIMANCHES A 13H 00).png',
        'QUESTIONS DE FEMMES (TOUS LES LUNDIS A 20H 40).png',
        'SOLEIL D_AFRIQUE (DU LUNDI AU VENDREDI A 11H 00).png'
    ]
    
    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LCA TV - Image Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .image-test { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }
        .image-test img { max-width: 300px; height: auto; display: block; margin: 10px 0; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>LCA TV - Image Display Test</h1>
    <p>This page tests if all required images are loading correctly.</p>
    
"""
    
    for i, image in enumerate(required_images, 1):
        html_content += f"""
    <div class="image-test">
        <h3>{i}. {image}</h3>
        <img src="static/images/{image}" alt="{image}" 
             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
        <div class="error" style="display:none;">❌ Image failed to load: {image}</div>
        <p>Direct link: <a href="static/images/{image}" target="_blank">static/images/{image}</a></p>
    </div>
"""
    
    html_content += """
    <script>
        // Check if images loaded successfully
        window.addEventListener('load', function() {
            const images = document.querySelectorAll('img');
            let loadedCount = 0;
            let totalCount = images.length;
            
            images.forEach(img => {
                if (img.complete && img.naturalHeight !== 0) {
                    loadedCount++;
                }
            });
            
            const result = document.createElement('div');
            result.style.cssText = 'margin: 20px 0; padding: 15px; border-radius: 5px; font-weight: bold;';
            
            if (loadedCount === totalCount) {
                result.className = 'success';
                result.style.backgroundColor = '#d4edda';
                result.innerHTML = `🎉 SUCCESS: All ${totalCount} images loaded correctly!`;
            } else {
                result.className = 'error';
                result.style.backgroundColor = '#f8d7da';
                result.innerHTML = `⚠️ WARNING: Only ${loadedCount}/${totalCount} images loaded correctly.`;
            }
            
            document.body.appendChild(result);
        });
    </script>
</body>
</html>"""
    
    with open('image_test.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print()
    print("📄 Generated image_test.html")
    print("   Upload this file and visit it in your browser to test image loading.")

if __name__ == "__main__":
    check_images()
    check_permissions()
    generate_test_html()
    
    print()
    print("🚀 Next Steps:")
    print("1. Fix any missing images")
    print("2. Upload all files to your server")
    print("3. Visit image_test.html to verify images load online")
    print("4. Check the deployment guide for more details")