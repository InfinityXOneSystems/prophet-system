"""
X1-Predict Infinity Portfolio System
====================================

Unlimited portfolio management with advanced features:
- Infinity portfolios (unlimited creation)
- Multiple risk profiles (conservative, moderate, risky, alpha)
- Flexible timeframes (day trading to multi-year)
- Paper trading, testnet, and mainnet support
- Advanced analytics and performance tracking
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import logging

logger = logging.getLogger('X1_PREDICT.PORTFOLIO')


class RiskProfile(Enum):
    """Risk profiles for portfolio management"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    RISKY = "risky"
    ALPHA_REWARD = "alpha_reward"


class Timeframe(Enum):
    """Trading timeframes"""
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "7d"
    DAY_15 = "15d"
    MONTH_1 = "30d"
    MONTH_2 = "60d"
    QUARTER = "90d"
    HALF_YEAR = "180d"
    YEAR_1 = "365d"
    YEAR_2 = "730d"
    CUSTOM = "custom"


class TradingEnvironment(Enum):
    """Trading environment types"""
    PAPER = "paper"
    TESTNET = "testnet"
    MAINNET = "mainnet"


@dataclass
class Position:
    """Represents a position in a portfolio"""
    symbol: str
    quantity: float
    entry_price: float
    entry_time: datetime
    current_price: float
    position_type: str = "long"  # long or short
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    position_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    @property
    def value(self) -> float:
        """Current position value"""
        return self.quantity * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Original cost basis"""
        return self.quantity * self.entry_price
    
    @property
    def pnl(self) -> float:
        """Profit/Loss in absolute terms"""
        if self.position_type == "long":
            return (self.current_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - self.current_price) * self.quantity
    
    @property
    def pnl_pct(self) -> float:
        """Profit/Loss in percentage"""
        if self.cost_basis == 0:
            return 0.0
        return (self.pnl / self.cost_basis) * 100
    
    @property
    def holding_period(self) -> timedelta:
        """How long the position has been held"""
        return datetime.now() - self.entry_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['entry_time'] = self.entry_time.isoformat()
        data['holding_period_hours'] = self.holding_period.total_seconds() / 3600
        data['value'] = self.value
        data['cost_basis'] = self.cost_basis
        data['pnl'] = self.pnl
        data['pnl_pct'] = self.pnl_pct
        return data


@dataclass
class PortfolioStrategy:
    """Trading strategy configuration"""
    strategy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Default Strategy"
    description: str = ""
    risk_profile: RiskProfile = RiskProfile.MODERATE
    timeframe: Timeframe = Timeframe.WEEK_1
    max_positions: int = 10
    max_position_size_pct: float = 10.0
    stop_loss_pct: float = 5.0
    take_profit_pct: float = 15.0
    diversification_min: int = 5
    rebalance_frequency: str = "daily"
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['risk_profile'] = self.risk_profile.value
        data['timeframe'] = self.timeframe.value
        data['created_at'] = self.created_at.isoformat()
        return data


@dataclass
class Portfolio:
    """
    Represents a trading portfolio with unlimited capabilities
    """
    portfolio_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Portfolio"
    description: str = ""
    initial_balance: float = 100000.0
    cash_balance: float = 100000.0
    environment: TradingEnvironment = TradingEnvironment.PAPER
    risk_profile: RiskProfile = RiskProfile.MODERATE
    strategies: List[PortfolioStrategy] = field(default_factory=list)
    positions: Dict[str, Position] = field(default_factory=dict)
    trade_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    tags: Set[str] = field(default_factory=set)
    
    @property
    def total_value(self) -> float:
        """Total portfolio value (cash + positions)"""
        positions_value = sum(pos.value for pos in self.positions.values())
        return self.cash_balance + positions_value
    
    @property
    def total_pnl(self) -> float:
        """Total profit/loss"""
        return self.total_value - self.initial_balance
    
    @property
    def total_pnl_pct(self) -> float:
        """Total profit/loss percentage"""
        if self.initial_balance == 0:
            return 0.0
        return (self.total_pnl / self.initial_balance) * 100
    
    @property
    def num_positions(self) -> int:
        """Number of open positions"""
        return len(self.positions)
    
    @property
    def positions_value(self) -> float:
        """Total value of all positions"""
        return sum(pos.value for pos in self.positions.values())
    
    @property
    def allocation_pct(self) -> float:
        """Percentage of capital allocated to positions"""
        if self.total_value == 0:
            return 0.0
        return (self.positions_value / self.total_value) * 100
    
    def add_position(self, position: Position) -> bool:
        """Add a position to the portfolio"""
        if position.symbol in self.positions:
            logger.warning(f"Position {position.symbol} already exists")
            return False
        
        # Check if we have enough cash
        required_cash = position.cost_basis
        if required_cash > self.cash_balance:
            logger.warning(f"Insufficient cash: required {required_cash}, available {self.cash_balance}")
            return False
        
        # Add position
        self.positions[position.symbol] = position
        self.cash_balance -= required_cash
        self.last_updated = datetime.now()
        
        # Record trade
        self.trade_history.append({
            'action': 'open',
            'symbol': position.symbol,
            'quantity': position.quantity,
            'price': position.entry_price,
            'timestamp': datetime.now().isoformat(),
            'position_id': position.position_id
        })
        
        logger.info(f"Added position {position.symbol}: {position.quantity} @ ${position.entry_price}")
        return True
    
    def close_position(self, symbol: str, exit_price: float) -> Optional[float]:
        """Close a position and return PnL"""
        if symbol not in self.positions:
            logger.warning(f"Position {symbol} not found")
            return None
        
        position = self.positions[symbol]
        
        # Calculate PnL
        position.current_price = exit_price
        pnl = position.pnl
        
        # Return cash
        exit_value = position.quantity * exit_price
        self.cash_balance += exit_value
        
        # Record trade
        self.trade_history.append({
            'action': 'close',
            'symbol': position.symbol,
            'quantity': position.quantity,
            'entry_price': position.entry_price,
            'exit_price': exit_price,
            'pnl': pnl,
            'pnl_pct': position.pnl_pct,
            'timestamp': datetime.now().isoformat(),
            'position_id': position.position_id
        })
        
        # Remove position
        del self.positions[symbol]
        self.last_updated = datetime.now()
        
        logger.info(f"Closed position {symbol}: PnL ${pnl:.2f} ({position.pnl_pct:.2f}%)")
        return pnl
    
    def update_prices(self, prices: Dict[str, float]):
        """Update current prices for all positions"""
        for symbol, price in prices.items():
            if symbol in self.positions:
                self.positions[symbol].current_price = price
        self.last_updated = datetime.now()
    
    def add_strategy(self, strategy: PortfolioStrategy):
        """Add a trading strategy"""
        self.strategies.append(strategy)
        logger.info(f"Added strategy '{strategy.name}' to portfolio {self.name}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate portfolio performance metrics"""
        if not self.trade_history:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0
            }
        
        # Analyze closed trades
        closed_trades = [t for t in self.trade_history if t['action'] == 'close']
        
        if not closed_trades:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0
            }
        
        wins = [t for t in closed_trades if t.get('pnl', 0) > 0]
        losses = [t for t in closed_trades if t.get('pnl', 0) <= 0]
        
        total_trades = len(closed_trades)
        win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0
        
        avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0
        
        total_wins = sum(t['pnl'] for t in wins)
        total_losses = abs(sum(t['pnl'] for t in losses))
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        # Calculate max drawdown
        balance_history = [self.initial_balance]
        running_balance = self.initial_balance
        
        for trade in closed_trades:
            running_balance += trade.get('pnl', 0)
            balance_history.append(running_balance)
        
        peak = balance_history[0]
        max_drawdown = 0
        
        for balance in balance_history:
            if balance > peak:
                peak = balance
            drawdown = ((peak - balance) / peak) * 100 if peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)
        
        return {
            'total_trades': total_trades,
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'total_pnl': self.total_pnl,
            'total_pnl_pct': self.total_pnl_pct
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert portfolio to dictionary"""
        return {
            'portfolio_id': self.portfolio_id,
            'name': self.name,
            'description': self.description,
            'environment': self.environment.value,
            'risk_profile': self.risk_profile.value,
            'initial_balance': self.initial_balance,
            'cash_balance': self.cash_balance,
            'total_value': self.total_value,
            'total_pnl': self.total_pnl,
            'total_pnl_pct': self.total_pnl_pct,
            'num_positions': self.num_positions,
            'positions_value': self.positions_value,
            'allocation_pct': self.allocation_pct,
            'positions': {symbol: pos.to_dict() for symbol, pos in self.positions.items()},
            'strategies': [s.to_dict() for s in self.strategies],
            'performance_metrics': self.get_performance_metrics(),
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'tags': list(self.tags)
        }


class InfinityPortfolioManager:
    """
    Infinity Portfolio Manager - Unlimited portfolio creation and management
    
    Features:
    - Unlimited portfolios
    - Unlimited strategies
    - Multiple risk profiles
    - Multiple trading environments
    - Advanced analytics
    - Performance tracking
    """
    
    def __init__(self, data_dir: str):
        """Initialize the portfolio manager"""
        self.data_dir = Path(data_dir)
        self.portfolios_dir = self.data_dir / 'portfolios'
        self.portfolios_dir.mkdir(parents=True, exist_ok=True)
        
        self.portfolios: Dict[str, Portfolio] = {}
        self._load_portfolios()
        
        logger.info(f"InfinityPortfolioManager initialized with {len(self.portfolios)} portfolios")
    
    def create_portfolio(
        self,
        name: str,
        initial_balance: float = 100000.0,
        environment: TradingEnvironment = TradingEnvironment.PAPER,
        risk_profile: RiskProfile = RiskProfile.MODERATE,
        description: str = "",
        tags: Optional[Set[str]] = None
    ) -> Portfolio:
        """Create a new portfolio"""
        portfolio = Portfolio(
            name=name,
            description=description,
            initial_balance=initial_balance,
            cash_balance=initial_balance,
            environment=environment,
            risk_profile=risk_profile,
            tags=tags or set()
        )
        
        self.portfolios[portfolio.portfolio_id] = portfolio
        self._save_portfolio(portfolio)
        
        logger.info(f"Created portfolio '{name}' with ID {portfolio.portfolio_id}")
        return portfolio
    
    def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """Get a portfolio by ID"""
        return self.portfolios.get(portfolio_id)
    
    def get_portfolio_by_name(self, name: str) -> Optional[Portfolio]:
        """Get a portfolio by name"""
        for portfolio in self.portfolios.values():
            if portfolio.name == name:
                return portfolio
        return None
    
    def list_portfolios(
        self,
        environment: Optional[TradingEnvironment] = None,
        risk_profile: Optional[RiskProfile] = None,
        tags: Optional[Set[str]] = None
    ) -> List[Portfolio]:
        """List portfolios with optional filters"""
        portfolios = list(self.portfolios.values())
        
        if environment:
            portfolios = [p for p in portfolios if p.environment == environment]
        
        if risk_profile:
            portfolios = [p for p in portfolios if p.risk_profile == risk_profile]
        
        if tags:
            portfolios = [p for p in portfolios if tags.issubset(p.tags)]
        
        return portfolios
    
    def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete a portfolio"""
        if portfolio_id not in self.portfolios:
            return False
        
        portfolio = self.portfolios[portfolio_id]
        
        # Remove file
        filepath = self.portfolios_dir / f"{portfolio_id}.json"
        if filepath.exists():
            filepath.unlink()
        
        # Remove from memory
        del self.portfolios[portfolio_id]
        
        logger.info(f"Deleted portfolio '{portfolio.name}' ({portfolio_id})")
        return True
    
    def get_aggregate_metrics(self) -> Dict[str, Any]:
        """Get aggregate metrics across all portfolios"""
        total_portfolios = len(self.portfolios)
        total_value = sum(p.total_value for p in self.portfolios.values())
        total_pnl = sum(p.total_pnl for p in self.portfolios.values())
        total_positions = sum(p.num_positions for p in self.portfolios.values())
        
        # Performance by environment
        by_environment = {}
        for env in TradingEnvironment:
            portfolios = [p for p in self.portfolios.values() if p.environment == env]
            if portfolios:
                by_environment[env.value] = {
                    'count': len(portfolios),
                    'total_value': sum(p.total_value for p in portfolios),
                    'total_pnl': sum(p.total_pnl for p in portfolios)
                }
        
        # Performance by risk profile
        by_risk = {}
        for risk in RiskProfile:
            portfolios = [p for p in self.portfolios.values() if p.risk_profile == risk]
            if portfolios:
                by_risk[risk.value] = {
                    'count': len(portfolios),
                    'total_value': sum(p.total_value for p in portfolios),
                    'total_pnl': sum(p.total_pnl for p in portfolios)
                }
        
        return {
            'total_portfolios': total_portfolios,
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_positions': total_positions,
            'by_environment': by_environment,
            'by_risk_profile': by_risk
        }
    
    def _save_portfolio(self, portfolio: Portfolio):
        """Save portfolio to disk"""
        filepath = self.portfolios_dir / f"{portfolio.portfolio_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(portfolio.to_dict(), f, indent=2)
    
    def _load_portfolios(self):
        """Load all portfolios from disk"""
        for filepath in self.portfolios_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Reconstruct portfolio (simplified - in production would be more robust)
                portfolio_id = data['portfolio_id']
                
                # Note: This is simplified - full implementation would reconstruct all objects
                logger.info(f"Loaded portfolio metadata: {data['name']} ({portfolio_id})")
                
            except Exception as e:
                logger.error(f"Error loading portfolio from {filepath}: {e}")
    
    def save_all(self):
        """Save all portfolios to disk"""
        for portfolio in self.portfolios.values():
            self._save_portfolio(portfolio)
        logger.info(f"Saved {len(self.portfolios)} portfolios")
