# X1-Predict Gamification System Guide

## 🎮 Overview

The X1-Predict Gamification System adds competitive leaderboards and the Infinity Coin token to create an engaging trading competition platform.

## ✨ Features

### 1. User Authentication
- Secure user registration and login
- Session management
- Profile tracking

### 2. Leaderboard Competition
Three competitive categories:
- **Highest Accuracy**: Best prediction accuracy (%)
- **Highest ROI**: Best return on investment (%)
- **Combined Score**: Weighted average of both (50%/50%)

### 3. Infinity Coin (INFI)
Official ERC-20 token with:
- 1 billion max supply
- Minting and burning capabilities
- Pausable for security
- Testnet deployment ready

## 🚀 Quick Start

### Basic Usage

```python
from src.features.gamification_manager import GamificationManager

# Initialize system
manager = GamificationManager('data')

# Register and login
result = manager.register_and_login(
    username="trader123",
    password="secure_password",
    email="trader@example.com"
)

session_id = result['session_id']

# Register portfolio for competition
manager.register_portfolio_for_competition(
    session_id=session_id,
    portfolio_id="portfolio_id_here",
    portfolio_name="My Trading Strategy"
)

# Update performance
manager.update_portfolio_performance(
    portfolio_id="portfolio_id_here",
    accuracy=75.5,
    roi=42.3,
    total_trades=150,
    winning_trades=110
)

# View leaderboards
leaderboards = manager.get_leaderboards(session_id, top_n=3)
```

### Deploy Infinity Coin

```python
# Deploy to testnet
result = manager.deploy_infinity_coin(
    session_id=session_id,
    network="ethereum_goerli"
)

print(f"Contract: {result['deployment']['contract_address']}")
print(f"Explorer: {result['explorer_url']}")
```

## 📊 Leaderboard Categories

### Accuracy Leaderboard
Ranks portfolios by prediction accuracy:
- Higher accuracy = better rank
- Minimum trades required: 10
- Formula: `(correct_predictions / total_predictions) * 100`

### ROI Leaderboard
Ranks portfolios by return on investment:
- Higher ROI = better rank
- Formula: `((current_value - initial_value) / initial_value) * 100`

### Combined Leaderboard
Ranks portfolios by combined score:
- Balances accuracy and profitability
- Formula: `(accuracy * 0.5) + (normalized_roi * 0.5)`

## 🏆 Competition Rules

### Testnet Competition (Current)
- All trades on testnets (Goerli, Sepolia, etc.)
- Practice with test tokens
- Learn and compete risk-free

### Future: Mainnet Competition
- Real cryptocurrency trading
- Real rewards
- Strict verification required

## 🪙 Infinity Coin Details

### Token Specifications
- **Name**: Infinity Coin
- **Symbol**: INFI
- **Decimals**: 18
- **Initial Supply**: 100,000,000 INFI
- **Max Supply**: 1,000,000,000 INFI

### Features
- **Mintable**: Owner can mint new tokens (up to max supply)
- **Burnable**: Users can burn their tokens
- **Pausable**: Emergency pause for security

### Deployment Networks
- Ethereum Goerli (testnet)
- Ethereum Sepolia (testnet)
- Binance Smart Chain Testnet
- Polygon Mumbai (testnet)

## 🎯 Getting on the Leaderboard

### Step 1: Create Account
```python
result = manager.register_and_login(
    username="your_username",
    password="your_password",
    email="your@email.com"
)
```

### Step 2: Register Portfolio
```python
manager.register_portfolio_for_competition(
    session_id=session_id,
    portfolio_id=portfolio.portfolio_id,
    portfolio_name="My Strategy"
)
```

### Step 3: Trade & Perform
- Make predictions
- Execute trades
- Build your track record

### Step 4: Climb the Ranks
- System automatically updates rankings
- Compete for top 3 positions
- Track your progress

## 📈 Performance Metrics

### Tracked Metrics
- **Accuracy**: Prediction success rate
- **ROI**: Portfolio returns
- **Total Trades**: Number of trades executed
- **Winning Trades**: Number of profitable trades
- **Total Value**: Current portfolio value
- **Profit/Loss**: Cumulative P&L

### How to Update
```python
manager.update_portfolio_performance(
    portfolio_id=portfolio_id,
    accuracy=85.2,          # %
    roi=45.7,               # %
    total_trades=200,
    winning_trades=170
)
```

## 🎨 Dashboard Integration

### Get Dashboard Data
```python
dashboard_data = manager.get_dashboard_data(session_id)

# Includes:
# - All leaderboards (top 3)
# - User rankings
# - Portfolio stats
# - Infinity Coin info
```

### Display Leaderboards
```python
leaderboards = manager.get_leaderboards(session_id, top_n=3)

for category, data in leaderboards['leaderboards'].items():
    print(f"\n{data['category_name']}")
    for entry in data['entries']:
        print(f"#{entry['rank']} {entry['username']}")
        print(f"  Score: {entry['score']:.2f}")
```

## 🔧 API Reference

### GamificationManager

#### register_and_login(username, password, email)
Register new user and auto-login.

#### login(username, password)
Login existing user.

#### register_portfolio_for_competition(session_id, portfolio_id, portfolio_name)
Register portfolio for leaderboard.

#### update_portfolio_performance(portfolio_id, accuracy, roi, total_trades, winning_trades)
Update portfolio metrics.

#### get_leaderboards(session_id, top_n)
Get all leaderboards.

#### get_user_profile(session_id)
Get user profile with rankings.

#### deploy_infinity_coin(session_id, network)
Deploy Infinity Coin to testnet.

## 🎯 Tips for Success

### Maximize Accuracy
- Use ensemble models
- Validate predictions
- Track historical performance
- Learn from mistakes

### Maximize ROI
- Proper risk management
- Diversify portfolio
- Take profits regularly
- Cut losses quickly

### Climb Combined Rankings
- Balance both accuracy and ROI
- Consistent performance
- Regular trading activity
- Learn continuously

## 🏅 Rewards (Future)

### Planned Reward System
- Top 3 in each category: INFI tokens
- Monthly champions: Special NFTs
- Yearly grand prize: Major rewards
- Streak bonuses: Consecutive wins

## 📞 Support

For questions or issues:
- Check documentation
- Review demo script: `gamification_demo.py`
- Test with: `python3 gamification_demo.py`

---

**Built with ❤️ by InfinityXOne Systems**
**Version**: 1.0.0 | **Date**: February 2026
