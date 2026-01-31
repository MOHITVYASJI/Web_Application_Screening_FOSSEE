#!/bin/bash
# Project Structure Verification Script
# This script verifies that all required files are present

echo "======================================"
echo "FOSSEE Project Structure Verification"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0

# Function to check file/directory
check_item() {
    TOTAL=$((TOTAL + 1))
    if [ -e "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $1 ${RED}(MISSING)${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "Checking root files..."
check_item "README.md"
check_item "SETUP_GUIDE.md"
check_item "PROJECT_STATUS.md"
check_item "sample_equipment_data.csv"
echo ""

echo "Checking backend structure..."
check_item "backend/manage.py"
check_item "backend/requirements.txt"
check_item "backend/config/settings.py"
check_item "backend/config/urls.py"
check_item "backend/config/wsgi.py"
check_item "backend/api/models.py"
check_item "backend/api/views.py"
check_item "backend/api/serializers.py"
check_item "backend/api/utils.py"
check_item "backend/api/urls.py"
echo ""

echo "Checking web frontend structure..."
check_item "web-frontend/package.json"
check_item "web-frontend/public/index.html"
check_item "web-frontend/src/index.js"
check_item "web-frontend/src/App.js"
check_item "web-frontend/src/App.css"
check_item "web-frontend/src/index.css"
check_item "web-frontend/src/services/api.js"
check_item "web-frontend/src/components/Auth/Login.js"
check_item "web-frontend/src/components/Auth/Register.js"
check_item "web-frontend/src/components/Dashboard/Dashboard.js"
check_item "web-frontend/src/components/Dashboard/UploadSection.js"
check_item "web-frontend/src/components/Dashboard/StatisticsCards.js"
check_item "web-frontend/src/components/Dashboard/ChartsSection.js"
check_item "web-frontend/src/components/Dashboard/DataTable.js"
check_item "web-frontend/src/components/Dashboard/DatasetHistory.js"
echo ""

echo "Checking desktop app structure..."
check_item "desktop-app/main.py"
check_item "desktop-app/requirements.txt"
check_item "desktop-app/components/login_window.py"
check_item "desktop-app/components/main_window.py"
check_item "desktop-app/components/data_table.py"
check_item "desktop-app/components/charts_widget.py"
check_item "desktop-app/utils/api_client.py"
echo ""

echo "======================================"
echo "VERIFICATION SUMMARY"
echo "======================================"
echo -e "Total items checked: ${YELLOW}${TOTAL}${NC}"
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo -e "${GREEN}✓ Project structure is complete and ready!${NC}"
    exit 0
else
    echo -e "${RED}✗ SOME CHECKS FAILED!${NC}"
    echo -e "${RED}✗ Please ensure all files are present.${NC}"
    exit 1
fi
