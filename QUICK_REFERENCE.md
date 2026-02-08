# X1-Predict Quick Reference Guide

## 🚀 Quick Start

### Option 1: Interactive Startup (Recommended for First Time)
```bash
./start_x1_predict.sh
```
- Interactive mode selection
- Guided configuration
- Automatic setup

### Option 2: Docker Compose (Production)
```bash
# Start all services
docker-compose -f docker-compose.x1predict.yml up -d

# View logs
docker-compose -f docker-compose.x1predict.yml logs -f x1-predict

# Stop all services
docker-compose -f docker-compose.x1predict.yml down
```

### Option 3: Direct Python
```bash
# Hybrid mode with moderate risk
python x1_predict.py --mode hybrid --risk moderate --dashboard

# Auto mode with risky profile
python x1_predict.py --mode auto --risk risky --cycle

# Check status
python x1_predict.py --status
```

---

## 🎛️ Configuration

### Environment File (.env)
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

### Key Settings
```yaml
# x1_predict_config.yaml

# Change mode
modes:
  current_mode: "hybrid"  # auto | hybrid | manual

# Change risk profile  
portfolios:
  risk_profiles:
    moderate:
      max_position_size: 10.0
      stop_loss_pct: 5.0

# Change trading environment
trading:
  mode: "paper"  # paper | testnet | mainnet
```

---

## 💼 Common Operations

### Create a Portfolio
```python
from src.trading.infinity_portfolio_system import (
    InfinityPortfolioManager, RiskProfile
)

manager = InfinityPortfolioManager('data')
portfolio = manager.create_portfolio(
    name="Growth Portfolio",
    initial_balance=100000.0,
    risk_profile=RiskProfile.MODERATE
)
```

### Create a Wallet
```python
from src.trading.wallet_system import (
    WalletSystem, BlockchainNetwork
)

wallet_sys = WalletSystem('data')

# Shadow wallet (auto-created)
shadow = wallet_sys.create_shadow_wallet(
    name="Trading Wallet",
    network=BlockchainNetwork.ETHEREUM_GOERLI
)

# Regular wallet (platform)
regular = wallet_sys.create_regular_wallet(
    name="Coinbase",
    platform=PlatformConnector.COINBASE,
    api_key="your_key"
)
```

### Create a Token
```python
from src.features.no_code_crypto_creator import (
    NoCodeCryptoCreator, TokenStandard
)

creator = NoCodeCryptoCreator('data')

# Step 1: Create project
project = creator.create_project(
    name="My Token",
    symbol="MTK",
    standard=TokenStandard.ERC20
)

# Step 2: Deploy
result = creator.deploy_project(
    project_id=project.project_id,
    deployer_address="0x...",
    network="ethereum_goerli"
)
```

### Run Scraping
```python
from src.scrapers.advanced_scraping_system import AdvancedScraper

scraper = AdvancedScraper('data', config)

# Run cycle
await scraper.run_scraping_cycle()

# Detect patterns
patterns = await scraper.detect_patterns(lookback_hours=24)
```

---

## 📊 Monitoring

### Access Points
- **Main Dashboard**: http://localhost:8080
- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090

### View Logs
```bash
# Local
tail -f logs/x1_predict.log

# Docker
docker-compose -f docker-compose.x1predict.yml logs -f x1-predict
```

### Check Health
```bash
# Via API
curl http://localhost:8080/health

# Via Python
python x1_predict.py --status
```

---

## 🎯 Mode Selection

### Auto Mode
- **Best for**: Experienced users, proven strategies
- **Risk**: High (system trades autonomously)
- **Setup**: `--mode auto`
- **Use when**: You trust the system completely

### Hybrid Mode (Recommended)
- **Best for**: Most users
- **Risk**: Medium (you approve trades)
- **Setup**: `--mode hybrid`
- **Use when**: You want AI help but final control

### Manual Mode
- **Best for**: Learning, testing
- **Risk**: Low (you control everything)
- **Setup**: `--mode manual`
- **Use when**: Getting familiar with the system

---

## 💰 Risk Profiles

### Conservative
```yaml
max_position_size: 5.0%
stop_loss: 2.0%
take_profit: 5.0%
min_diversification: 10 assets
```
- **Best for**: Capital preservation
- **Expected return**: 5-10% annually
- **Risk level**: ★☆☆☆☆

### Moderate (Recommended)
```yaml
max_position_size: 10.0%
stop_loss: 5.0%
take_profit: 15.0%
min_diversification: 7 assets
```
- **Best for**: Balanced growth
- **Expected return**: 15-30% annually
- **Risk level**: ★★★☆☆

### Risky
```yaml
max_position_size: 20.0%
stop_loss: 10.0%
take_profit: 30.0%
min_diversification: 5 assets
```
- **Best for**: Aggressive growth
- **Expected return**: 30-60% annually
- **Risk level**: ★★★★☆

### Alpha Reward
```yaml
max_position_size: 50.0%
stop_loss: 20.0%
take_profit: 100.0%
min_diversification: 3 assets
```
- **Best for**: Maximum returns
- **Expected return**: 100%+ annually
- **Risk level**: ★★★★★

---

## 🕐 Timeframe Selection

```yaml
# Intraday
"1h", "4h"          # Day trading

# Short-term
"1d", "3d", "7d"    # Swing trading

# Medium-term  
"15d", "30d", "60d", "90d"  # Position trading

# Long-term
"180d", "365d"      # Investing
```

---

## 🔧 Troubleshooting

### System Won't Start
```bash
# Check logs
tail -f logs/x1_predict.log

# Verify dependencies
pip install -r requirements.txt

# Check Docker
docker ps -a
```

### Database Connection Issues
```bash
# Restart databases
docker-compose -f docker-compose.x1predict.yml restart redis postgres mongodb

# Check connectivity
docker-compose -f docker-compose.x1predict.yml exec redis redis-cli ping
```

### Scraper Not Working
```bash
# Install Playwright browsers
playwright install chromium

# Test manually
python -m src.scrapers.advanced_scraping_system
```

### Low Prediction Accuracy
1. Check data quality
2. Increase training data
3. Adjust model parameters
4. Review recent market conditions
5. Consider model retraining

---

## 📝 Best Practices

### 1. Start Small
- Begin with paper trading
- Use TestNet for crypto
- Start with conservative risk
- Increase gradually

### 2. Monitor Regularly
- Check dashboard daily
- Review performance weekly
- Analyze trades monthly
- Adjust strategy quarterly

### 3. Risk Management
- Never risk more than 2% per trade
- Diversify across assets
- Use stop losses
- Take profits regularly

### 4. Continuous Learning
- Review trade history
- Learn from mistakes
- Update strategies
- Stay informed

---

## 🆘 Emergency Procedures

### Stop All Trading
```python
# Via code
x1.set_mode('manual')

# Via Docker
docker-compose -f docker-compose.x1predict.yml stop x1-predict
```

### Emergency Exit All Positions
```python
portfolio = manager.get_portfolio(portfolio_id)
for symbol in list(portfolio.positions.keys()):
    portfolio.close_position(symbol, current_price)
```

### Rollback Configuration
```bash
# Restore backup config
cp x1_predict_config.yaml.backup x1_predict_config.yaml

# Restart system
docker-compose -f docker-compose.x1predict.yml restart
```

---

## 📞 Support Resources

### Documentation
- **Architecture**: X1_PREDICT_ARCHITECTURE.md
- **User Guide**: README_X1_PREDICT.md
- **Runbook**: RUNBOOK_SECRETS.md
- **Summary**: IMPLEMENTATION_SUMMARY.md

### Common Commands
```bash
# Status
python x1_predict.py --status

# Run cycle
python x1_predict.py --cycle

# Start dashboard
python x1_predict.py --dashboard --port 8080

# Check Docker services
docker-compose -f docker-compose.x1predict.yml ps

# View logs
docker-compose -f docker-compose.x1predict.yml logs -f

# Restart service
docker-compose -f docker-compose.x1predict.yml restart x1-predict
```

---

## 🎓 Learning Path

### Week 1: Familiarization
- Read documentation
- Explore dashboard
- Try manual mode
- Create test portfolio

### Week 2: Paper Trading
- Switch to hybrid mode
- Start paper trading
- Monitor predictions
- Review results

### Week 3: Strategy Development
- Test different timeframes
- Try various risk profiles
- Analyze performance
- Optimize settings

### Week 4: TestNet Practice
- Deploy to TestNet
- Real transactions (test money)
- Validate strategies
- Build confidence

### Month 2+: Gradual Scaling
- Consider mainnet
- Start with conservative
- Increase gradually
- Continuous improvement

---

## ✅ Pre-Deployment Checklist

- [ ] Configuration reviewed
- [ ] API keys configured
- [ ] Risk profile selected
- [ ] Mode chosen appropriately
- [ ] Backup strategy in place
- [ ] Monitoring setup verified
- [ ] Emergency procedures understood
- [ ] Documentation reviewed
- [ ] Test on paper/TestNet first

---

**Remember**: Start small, learn continuously, manage risk carefully, and scale gradually!
