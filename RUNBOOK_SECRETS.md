# X1-Predict Operational Runbook
# Secrets, Tips & Tricks for Maximum Accuracy and Profit

## 🎯 Core Philosophy

X1-Predict is designed to maximize prediction accuracy and profit through:
1. **Precision over Volume**: Quality predictions > quantity
2. **Risk Management**: Protect capital first, profit second
3. **Continuous Learning**: Every trade teaches the system
4. **Multi-Timeline Thinking**: Consider all possible futures

---

## 🔐 Insider Secrets

### Secret #1: The Golden Hour
**What**: First hour after major market opens (9:30 AM EST, 8:00 AM UTC for crypto)  
**Why**: Maximum volatility = maximum opportunity  
**How**: Configure scrapers to intensify during these periods

```yaml
# In x1_predict_config.yaml
data_acquisition:
  golden_hour:
    enabled: true
    times: ["09:30-10:30 EST", "08:00-09:00 UTC"]
    scraping_frequency_multiplier: 5.0
```

### Secret #2: Sentiment Reversal Indicator
**What**: When 80%+ social sentiment is extreme, reversal is near  
**Why**: Markets are contrarian at extremes  
**How**: Monitor sentiment aggregation

```python
# Check for reversal opportunity
sentiment_data = scraper.get_sentiment_summary(hours=24)
if sentiment_data['bullish_pct'] > 80:
    # Consider short position
    logger.info("REVERSAL SIGNAL: Extreme bullishness detected")
elif sentiment_data['bearish_pct'] > 80:
    # Consider long position
    logger.info("REVERSAL SIGNAL: Extreme bearishness detected")
```

### Secret #3: The 3-Day Rule
**What**: Wait 3 days after major news before acting  
**Why**: Initial reactions are often wrong  
**How**: Implement news cooldown period

```python
# In trading logic
if major_news_detected:
    cooldown_until = datetime.now() + timedelta(days=3)
    logger.info(f"News cooldown active until {cooldown_until}")
```

### Secret #4: Volume Precedes Price
**What**: Volume spikes 1-3 hours before price moves  
**Why**: Smart money moves first  
**How**: Monitor volume anomalies

```python
# Volume spike detection
current_volume = get_current_volume(symbol)
avg_volume = get_average_volume(symbol, hours=24)

if current_volume > avg_volume * 2.5:
    logger.warning(f"VOLUME SPIKE: {symbol} - Prepare for price movement")
```

### Secret #5: Multi-Timeframe Confirmation
**What**: Only trade when 3+ timeframes agree  
**Why**: Reduces false signals by 70%  
**How**: Check alignment

```python
# Multi-timeframe analysis
timeframes = ['1h', '4h', '1d']
signals = [get_signal(symbol, tf) for tf in timeframes]

if signals.count('bullish') >= 3:
    logger.info(f"STRONG SIGNAL: {symbol} bullish across all timeframes")
```

---

## 💡 Pro Tips

### Tip #1: Portfolio Diversification Sweet Spot
- **Conservative**: 12-15 positions
- **Moderate**: 8-10 positions
- **Risky**: 5-7 positions
- **Alpha**: 3-5 positions (concentrated bets)

### Tip #2: Best Times to Trade
1. **Stocks**: 9:30-10:30 AM, 3:30-4:00 PM EST
2. **Crypto**: 8:00-10:00 AM, 8:00-10:00 PM UTC
3. **Forex**: London open (3:00 AM EST), NY open (8:00 AM EST)

### Tip #3: Stop Loss Placement
- **Technical**: Just below recent support
- **Volatility-based**: 1.5x ATR (Average True Range)
- **Time-based**: Exit if no movement in 48 hours

```python
# Calculate optimal stop loss
atr = calculate_atr(symbol, periods=14)
entry_price = 100.0
stop_loss = entry_price - (atr * 1.5)
```

### Tip #4: Position Sizing Formula
```python
# Kelly Criterion (adjusted)
win_rate = 0.60  # 60% win rate
avg_win = 1.5    # Average 50% gain
avg_loss = 1.0   # Average 100% loss

kelly_pct = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
position_size = kelly_pct * 0.5  # Use half Kelly for safety
```

### Tip #5: Correlation Trading
- Don't hold highly correlated assets (>0.8)
- Use negative correlation for hedging
- Check correlation matrix weekly

---

## 🎓 Advanced Strategies

### Strategy #1: Mean Reversion
**Best for**: Ranging markets  
**Timeframe**: 1-7 days  
**Win Rate**: ~65%

```python
# Mean reversion setup
def is_oversold(symbol):
    rsi = calculate_rsi(symbol, periods=14)
    bb_lower = get_bollinger_band_lower(symbol)
    current_price = get_price(symbol)
    
    return rsi < 30 and current_price < bb_lower
```

### Strategy #2: Trend Following
**Best for**: Strong trending markets  
**Timeframe**: 7-30 days  
**Win Rate**: ~55% (but large winners)

```python
# Trend following setup
def is_strong_trend(symbol):
    ema_50 = calculate_ema(symbol, periods=50)
    ema_200 = calculate_ema(symbol, periods=200)
    current_price = get_price(symbol)
    
    return current_price > ema_50 > ema_200  # Bullish trend
```

### Strategy #3: Breakout Trading
**Best for**: Consolidation followed by expansion  
**Timeframe**: 1-3 days  
**Win Rate**: ~50% (but explosive when right)

```python
# Breakout detection
def is_breakout(symbol):
    resistance = get_resistance_level(symbol)
    volume = get_current_volume(symbol)
    avg_volume = get_average_volume(symbol, hours=24)
    current_price = get_price(symbol)
    
    return (current_price > resistance and 
            volume > avg_volume * 2.0)
```

### Strategy #4: Arbitrage
**Best for**: Crypto across exchanges  
**Timeframe**: Seconds to minutes  
**Win Rate**: ~90% (but small gains)

```python
# Cross-exchange arbitrage
def find_arbitrage_opportunity():
    btc_binance = get_price('BTC', 'binance')
    btc_coinbase = get_price('BTC', 'coinbase')
    
    spread_pct = abs(btc_binance - btc_coinbase) / btc_binance * 100
    
    if spread_pct > 0.5:  # 0.5% spread
        return {
            'buy_from': 'binance' if btc_binance < btc_coinbase else 'coinbase',
            'sell_to': 'coinbase' if btc_binance < btc_coinbase else 'binance',
            'profit_pct': spread_pct
        }
```

---

## 🚨 Risk Management Rules

### Rule #1: Never Risk More Than 2% Per Trade
```python
account_size = 100000
risk_per_trade = account_size * 0.02  # $2,000
entry_price = 100
stop_loss = 95

position_size = risk_per_trade / (entry_price - stop_loss)
# position_size = $2,000 / $5 = 400 shares
```

### Rule #2: Maximum Drawdown Limit
- Stop trading if down 10% in a month
- Review strategy
- Paper trade until confident again

### Rule #3: Diversification Limits
- Max 25% in single asset
- Max 40% in single sector
- Max 60% in single asset class

### Rule #4: Time-Based Exits
- Exit if position doesn't move as expected within timeframe
- Don't hold losers hoping they'll recover
- Cut losses quickly, let winners run

---

## 📊 Performance Optimization

### Optimization #1: Prediction Confidence Threshold
```python
# Only trade high-confidence predictions
MIN_CONFIDENCE = 0.75

prediction = x1.predict(symbol)
if prediction['confidence'] >= MIN_CONFIDENCE:
    execute_trade(prediction)
else:
    logger.info(f"Skipping {symbol} - confidence too low")
```

### Optimization #2: Backtesting Before Live
```python
# Always backtest new strategies
from src.validation.backtester import Backtester

backtester = Backtester()
results = backtester.run_strategy(
    strategy=my_strategy,
    start_date='2023-01-01',
    end_date='2024-01-01'
)

if results['sharpe_ratio'] > 1.5 and results['win_rate'] > 0.55:
    logger.info("Strategy validated - ready for live trading")
```

### Optimization #3: Model Retraining Schedule
- Daily: Quick updates with latest data
- Weekly: Full retraining with hyperparameter tuning
- Monthly: Model architecture review

### Optimization #4: Feature Engineering
```python
# Add powerful features
def create_features(df):
    # Price-based
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(20).std()
    
    # Volume-based
    df['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
    
    # Time-based
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    
    # Technical indicators
    df['rsi'] = calculate_rsi(df)
    df['macd'] = calculate_macd(df)
    
    return df
```

---

## 🔧 System Tuning

### Tuning #1: Scraper Frequency
```yaml
# High-frequency for fast-moving assets
bitcoin:
  frequency_minutes: 5
  
# Lower frequency for stable assets
blue_chip_stocks:
  frequency_minutes: 60
```

### Tuning #2: Agent Priorities
```python
# Adjust based on market conditions
if market_volatile:
    risk_manager.priority = 'critical'
    market_analyst.priority = 'high'
elif market_stable:
    pattern_recognizer.priority = 'high'
    risk_manager.priority = 'medium'
```

### Tuning #3: Memory Management
```python
# Clean old data periodically
def cleanup_old_data(days=90):
    cutoff = datetime.now() - timedelta(days=days)
    
    # Remove old scraped data
    old_data = [d for d in scraped_data if d.scraped_at < cutoff]
    for data in old_data:
        delete_data(data)
    
    logger.info(f"Cleaned up {len(old_data)} old records")
```

---

## 🎯 Accuracy Boosters

### Booster #1: Ensemble Predictions
Use multiple models and vote:
```python
models = ['automl', 'lstm', 'xgboost', 'prophet']
predictions = [model.predict(symbol) for model in models]

# Weighted voting
final_prediction = weighted_average(predictions, weights=[0.3, 0.25, 0.25, 0.2])
```

### Booster #2: Out-of-Sample Testing
```python
# Always test on unseen data
train_data = data[:int(len(data) * 0.7)]
validation_data = data[int(len(data) * 0.7):int(len(data) * 0.85)]
test_data = data[int(len(data) * 0.85):]

# Never touch test_data until final validation
```

### Booster #3: Walk-Forward Analysis
```python
# Continuously retrain as new data comes in
for date in date_range:
    train_window = get_data(date - timedelta(days=365), date)
    model.train(train_window)
    
    test_window = get_data(date, date + timedelta(days=7))
    performance = model.evaluate(test_window)
    
    if performance['accuracy'] < 0.60:
        logger.warning("Model performance degraded - retraining")
```

---

## 📈 Profit Maximization

### Maximizer #1: Compound Returns
```python
# Reinvest profits automatically
def compound_profits():
    portfolio_value = get_portfolio_value()
    profit = portfolio_value - initial_balance
    
    if profit > 0:
        # Reinvest 80% of profits
        reinvest_amount = profit * 0.8
        add_to_trading_capital(reinvest_amount)
```

### Maximizer #2: Scale In/Out
```python
# Don't enter full position at once
def scale_in(symbol, total_size):
    # Enter in 3 tranches
    sizes = [total_size * 0.4, total_size * 0.3, total_size * 0.3]
    
    for size in sizes:
        if conditions_still_valid():
            execute_trade(symbol, size)
            wait(hours=4)
```

### Maximizer #3: Tax Optimization
- Hold winners >1 year for long-term capital gains
- Harvest losses for tax deductions
- Use tax-advantaged accounts

---

## 🌟 Pro Insider Knowledge

### Insight #1: Market Psychology
- Fear > Greed in terms of impact
- FOMO (Fear of Missing Out) creates tops
- Panic creates bottoms

### Insight #2: Smart Money Indicators
- Watch institutional 13F filings
- Monitor options flow (large unusual orders)
- Track whale wallet movements (crypto)

### Insight #3: Seasonal Patterns
- "Sell in May and go away" (stocks)
- "Santa Rally" (late December)
- "Chinese New Year" effect (crypto)

### Insight #4: News Hierarchy
Impact from highest to lowest:
1. Federal Reserve decisions
2. Regulatory changes
3. Major hacks/security breaches
4. Partnership announcements
5. Influencer tweets

---

## 🚀 Advanced Techniques

### Technique #1: Meta-Learning
```python
# Learn which strategies work in which conditions
strategy_performance = {}

for strategy in strategies:
    for market_condition in conditions:
        perf = backtest(strategy, market_condition)
        strategy_performance[(strategy, market_condition)] = perf

# Use best strategy for current condition
current_condition = detect_market_condition()
best_strategy = max(
    strategies,
    key=lambda s: strategy_performance.get((s, current_condition), 0)
)
```

### Technique #2: Adversarial Testing
```python
# Test against worst-case scenarios
worst_case_scenarios = [
    'flash_crash',
    'black_swan_event',
    'exchange_hack',
    'regulatory_crackdown'
]

for scenario in worst_case_scenarios:
    result = simulate_scenario(portfolio, scenario)
    if result['max_loss'] > acceptable_loss:
        logger.warning(f"Portfolio vulnerable to {scenario}")
```

### Technique #3: Adaptive Position Sizing
```python
# Adjust position size based on recent performance
def adaptive_position_size(base_size, recent_win_rate):
    if recent_win_rate > 0.65:
        return base_size * 1.2  # Increase when hot
    elif recent_win_rate < 0.45:
        return base_size * 0.5  # Decrease when cold
    else:
        return base_size  # Keep normal
```

---

## 📚 Continuous Improvement

### Improvement #1: Daily Review
- Review all trades (winners and losers)
- Document what worked/didn't work
- Update strategy rules

### Improvement #2: Weekly Analysis
- Performance metrics review
- Strategy effectiveness analysis
- Model accuracy check

### Improvement #3: Monthly Deep Dive
- Full portfolio review
- Rebalancing needs
- Strategy rotation
- Model retraining

---

**Remember**: This runbook is a living document. Update it as you learn and discover new insights!
