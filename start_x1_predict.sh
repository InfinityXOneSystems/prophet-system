#!/bin/bash
# X1-Predict Startup Script
# FAANG Enterprise-Grade System

set -e

echo "============================================="
echo "  X1-PREDICT STARTUP"
echo "  Enterprise Quantum Predictor v1.0.0"
echo "============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_warning "Creating .env from template..."
    
    cat > .env << 'EOF'
# X1-Predict Environment Configuration

# System Configuration
X1_MODE=hybrid
X1_RISK_PROFILE=moderate
X1_ENVIRONMENT=production

# Google Cloud Platform
GCP_PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Admin Control Plane
ADMIN_CONTROL_PLANE_URL=http://localhost:8082
ADMIN_API_KEY=your-admin-api-key

# Database Passwords
REDIS_PASSWORD=your-redis-password
POSTGRES_PASSWORD=your-postgres-password
MONGO_PASSWORD=your-mongo-password
GRAFANA_PASSWORD=your-grafana-password

# API Keys (Optional)
COINBASE_API_KEY=
COINBASE_API_SECRET=
BINANCE_API_KEY=
BINANCE_API_SECRET=
KRAKEN_API_KEY=
KRAKEN_API_SECRET=
ALPACA_API_KEY=
ALPACA_API_SECRET=

# Social Media API Keys (Optional)
TWITTER_API_KEY=
TWITTER_API_SECRET=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=

# Monitoring
ENABLE_MONITORING=true
ENABLE_ALERTS=true
ALERT_EMAIL=alerts@example.com
EOF
    
    print_status ".env file created. Please edit it with your credentials."
    print_warning "Run this script again after configuring .env"
    exit 1
fi

print_status "Environment configuration found"

# Load environment variables
source .env

# Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi
print_status "Python $PYTHON_VERSION detected"

# Check if Docker is installed
if command -v docker &> /dev/null; then
    print_status "Docker is installed"
    DOCKER_MODE=true
else
    print_warning "Docker not found. Will run in local mode."
    DOCKER_MODE=false
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p data/{portfolios,wallets,crypto_projects,scraped_data,autonomous_cycles,knowledge_base}
mkdir -p logs
mkdir -p config
print_status "Directories created"

# Install/Update dependencies
print_status "Checking dependencies..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
print_status "Virtual environment activated"

print_status "Installing/updating dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
pip install -r reflection_requirements.txt > /dev/null 2>&1
print_status "Dependencies installed"

# Install Playwright browsers if needed
if ! python -c "import playwright" &> /dev/null; then
    print_status "Installing Playwright browsers..."
    playwright install chromium
fi

# Check configuration
print_status "Validating configuration..."
if python3 -c "
import yaml
with open('x1_predict_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print('Configuration valid')
" 2>&1; then
    print_status "Configuration is valid"
else
    print_error "Configuration validation failed"
    exit 1
fi

# Startup mode selection
echo ""
echo "Select startup mode:"
echo "1) Auto Mode (Fully autonomous)"
echo "2) Hybrid Mode (AI + Human approval) [RECOMMENDED]"
echo "3) Manual Mode (Full human control)"
echo "4) Docker Compose (Full stack)"
echo "5) Status Check Only"
echo ""
read -p "Enter choice [1-5]: " MODE_CHOICE

case $MODE_CHOICE in
    1)
        STARTUP_MODE="auto"
        print_warning "Auto mode selected - System will trade autonomously!"
        ;;
    2)
        STARTUP_MODE="hybrid"
        print_status "Hybrid mode selected - AI recommendations with approval"
        ;;
    3)
        STARTUP_MODE="manual"
        print_status "Manual mode selected - You have full control"
        ;;
    4)
        if [ "$DOCKER_MODE" = true ]; then
            print_status "Starting Docker Compose stack..."
            docker-compose -f docker-compose.x1predict.yml up -d
            print_status "Docker stack started!"
            print_status "Dashboard: http://localhost:8080"
            print_status "Grafana: http://localhost:3001"
            echo ""
            echo "To view logs: docker-compose -f docker-compose.x1predict.yml logs -f"
            exit 0
        else
            print_error "Docker not available"
            exit 1
        fi
        ;;
    5)
        print_status "Running status check..."
        python3 x1_predict.py --status
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Risk profile selection
echo ""
echo "Select risk profile:"
echo "1) Conservative (Low risk, stable returns)"
echo "2) Moderate (Balanced) [RECOMMENDED]"
echo "3) Risky (Higher risk, higher returns)"
echo "4) Alpha Reward (Maximum risk & returns)"
echo ""
read -p "Enter choice [1-4]: " RISK_CHOICE

case $RISK_CHOICE in
    1) RISK_PROFILE="conservative" ;;
    2) RISK_PROFILE="moderate" ;;
    3) RISK_PROFILE="risky" ;;
    4) RISK_PROFILE="alpha_reward" ;;
    *) 
        print_error "Invalid choice"
        exit 1
        ;;
esac

print_status "Configuration: Mode=$STARTUP_MODE, Risk=$RISK_PROFILE"

# Final confirmation
echo ""
print_warning "Ready to start X1-Predict with the following settings:"
echo "  Mode: $STARTUP_MODE"
echo "  Risk Profile: $RISK_PROFILE"
echo "  Environment: $X1_ENVIRONMENT"
echo ""
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    print_status "Startup cancelled"
    exit 0
fi

# Start the system
echo ""
print_status "Starting X1-Predict..."
echo ""

# Start in background with nohup
nohup python3 x1_predict.py \
    --mode "$STARTUP_MODE" \
    --risk "$RISK_PROFILE" \
    --dashboard \
    > logs/x1_predict.log 2>&1 &

PID=$!
echo $PID > x1_predict.pid

print_status "X1-Predict started (PID: $PID)"
print_status "Dashboard will be available at: http://localhost:8080"
print_status "Logs: tail -f logs/x1_predict.log"
echo ""
print_status "To stop: kill \$(cat x1_predict.pid)"
echo ""

# Wait a moment and check if it's running
sleep 3

if ps -p $PID > /dev/null; then
    print_status "System is running successfully!"
    echo ""
    echo "Quick Commands:"
    echo "  Status:  python3 x1_predict.py --status"
    echo "  Logs:    tail -f logs/x1_predict.log"
    echo "  Stop:    kill \$(cat x1_predict.pid)"
    echo ""
else
    print_error "System failed to start. Check logs/x1_predict.log"
    exit 1
fi

print_status "X1-Predict is now operational!"
echo "============================================="
