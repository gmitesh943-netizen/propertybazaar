#!/bin/bash
# =====================================================================
# PropertyBazaar - PythonAnywhere Auto Setup Script
# =====================================================================
# USAGE:
#   1. Open PythonAnywhere → Consoles → Bash
#   2. Run: bash <(curl -s https://raw.githubusercontent.com/gmitesh943-netizen/propertybazaar/main/pythonanywhere_setup.sh)
#   OR manually paste and run this script
# =====================================================================

set -e  # Exit on any error

echo "=============================================="
echo "  PropertyBazaar - PythonAnywhere Setup"
echo "=============================================="

# ---- CONFIG (Change these!) ----
GITHUB_REPO="https://github.com/gmitesh943-netizen/propertybazaar.git"
PROJECT_DIR="propertybazaar"
PYTHON_VER="python3.10"   # PythonAnywhere free tier supports 3.10
# --------------------------------

echo ""
echo "Step 1: Cloning project from GitHub..."
if [ -d "$PROJECT_DIR" ]; then
    echo "  → Folder exists, pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull origin main
    cd ..
else
    git clone "$GITHUB_REPO" "$PROJECT_DIR"
fi

echo ""
echo "Step 2: Creating Virtual Environment..."
cd "$PROJECT_DIR"
$PYTHON_VER -m venv venv
source venv/bin/activate

echo ""
echo "Step 3: Installing Requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Step 4: Creating .env file..."
cat > .env << 'ENVFILE'
SECRET_KEY=CHANGE-THIS-TO-A-STRONG-SECRET-KEY-50-CHARS
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
ENVFILE

echo ""
echo "  ⚠️  IMPORTANT: Edit .env file with your actual values!"
echo "  Run: nano .env"
echo ""
read -p "  Press ENTER after you have edited .env to continue..."

echo ""
echo "Step 5: Running Migrations..."
python manage.py migrate --noinput

echo ""
echo "Step 6: Collecting Static Files..."
python manage.py collectstatic --noinput

echo ""
echo "Step 7: Creating Superuser (Admin)..."
echo "  You can create admin user now:"
python manage.py createsuperuser

echo ""
echo "=============================================="
echo "  ✅ Setup Complete!"
echo "=============================================="
echo ""
echo "  NOW DO THESE MANUAL STEPS in Web Tab:"
echo ""
echo "  1. Source Code:    /home/\$USER/$PROJECT_DIR"
echo "  2. Working Dir:    /home/\$USER/$PROJECT_DIR"
echo "  3. Virtualenv:     /home/\$USER/$PROJECT_DIR/venv"
echo "  4. Static URL:     /static/"
echo "     Static Dir:     /home/\$USER/$PROJECT_DIR/staticfiles"
echo "  5. Media URL:      /media/"
echo "     Media Dir:      /home/\$USER/$PROJECT_DIR/media"
echo ""
echo "  6. WSGI File: Paste content from pythonanywhere_wsgi.py"
echo "     (replace YOUR_USERNAME with: \$USER)"
echo ""
echo "  7. Click RELOAD ✅"
echo ""
echo "  🌐 Your site: https://\$USER.pythonanywhere.com"
echo "=============================================="
