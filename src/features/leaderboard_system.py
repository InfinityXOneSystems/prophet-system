"""
Leaderboard Gamification System
================================

Competitive leaderboard system for tracking top performers.
Three categories: Highest Accuracy, Highest ROI, and Combined Score.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import logging

logger = logging.getLogger('X1_PREDICT.LEADERBOARD')


class LeaderboardCategory(Enum):
    """Leaderboard categories"""
    ACCURACY = "accuracy"
    ROI = "roi"
    COMBINED = "combined"


@dataclass
class PortfolioPerformance:
    """Portfolio performance metrics"""
    portfolio_id: str
    user_id: str
    username: str
    portfolio_name: str
    
    # Performance metrics
    accuracy: float = 0.0  # Prediction accuracy (0-100%)
    roi: float = 0.0  # Return on Investment (%)
    combined_score: float = 0.0  # Combined score
    
    # Additional stats
    total_trades: int = 0
    winning_trades: int = 0
    total_value: float = 0.0
    profit_loss: float = 0.0
    
    # Tracking
    last_updated: datetime = field(default_factory=datetime.now)
    
    def calculate_combined_score(self):
        """Calculate combined score (50% accuracy + 50% normalized ROI)"""
        # Normalize ROI to 0-100 scale (assuming -100% to +200% range)
        normalized_roi = max(0, min(100, (self.roi + 100) / 3))
        self.combined_score = (self.accuracy * 0.5) + (normalized_roi * 0.5)
        return self.combined_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'portfolio_id': self.portfolio_id,
            'user_id': self.user_id,
            'username': self.username,
            'portfolio_name': self.portfolio_name,
            'accuracy': round(self.accuracy, 2),
            'roi': round(self.roi, 2),
            'combined_score': round(self.combined_score, 2),
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'total_value': round(self.total_value, 2),
            'profit_loss': round(self.profit_loss, 2),
            'last_updated': self.last_updated.isoformat()
        }


@dataclass
class LeaderboardEntry:
    """Leaderboard entry"""
    rank: int
    portfolio_id: str
    user_id: str
    username: str
    portfolio_name: str
    score: float
    accuracy: float
    roi: float
    total_trades: int
    is_testnet: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'rank': self.rank,
            'portfolio_id': self.portfolio_id,
            'user_id': self.user_id,
            'username': self.username,
            'portfolio_name': self.portfolio_name,
            'score': round(self.score, 2),
            'accuracy': round(self.accuracy, 2),
            'roi': round(self.roi, 2),
            'total_trades': self.total_trades,
            'is_testnet': self.is_testnet
        }


class LeaderboardSystem:
    """
    Leaderboard Gamification System
    
    Features:
    - Track portfolio performance across users
    - Rank top 3 in each category
    - Support testnet and mainnet competitions
    - Real-time updates
    """
    
    def __init__(self, data_dir: str):
        """Initialize leaderboard system"""
        self.data_dir = Path(data_dir)
        self.leaderboard_dir = self.data_dir / 'leaderboards'
        self.performance_dir = self.data_dir / 'performance'
        
        self.leaderboard_dir.mkdir(parents=True, exist_ok=True)
        self.performance_dir.mkdir(parents=True, exist_ok=True)
        
        self.performances: Dict[str, PortfolioPerformance] = {}
        self._load_performances()
        
        logger.info(f"LeaderboardSystem initialized with {len(self.performances)} portfolios")
    
    def register_portfolio(
        self,
        portfolio_id: str,
        user_id: str,
        username: str,
        portfolio_name: str
    ) -> PortfolioPerformance:
        """
        Register a portfolio for leaderboard tracking
        
        Args:
            portfolio_id: Portfolio ID
            user_id: User ID
            username: Username
            portfolio_name: Portfolio name
            
        Returns:
            PortfolioPerformance object
        """
        if portfolio_id in self.performances:
            return self.performances[portfolio_id]
        
        perf = PortfolioPerformance(
            portfolio_id=portfolio_id,
            user_id=user_id,
            username=username,
            portfolio_name=portfolio_name
        )
        
        self.performances[portfolio_id] = perf
        self._save_performance(perf)
        
        logger.info(f"Registered portfolio for leaderboard: {portfolio_name} ({username})")
        return perf
    
    def update_performance(
        self,
        portfolio_id: str,
        accuracy: float = None,
        roi: float = None,
        total_trades: int = None,
        winning_trades: int = None,
        total_value: float = None,
        profit_loss: float = None
    ) -> bool:
        """
        Update portfolio performance metrics
        
        Args:
            portfolio_id: Portfolio ID
            accuracy: Prediction accuracy (0-100%)
            roi: Return on investment (%)
            total_trades: Total number of trades
            winning_trades: Number of winning trades
            total_value: Current portfolio value
            profit_loss: Total profit/loss
            
        Returns:
            True if successful
        """
        perf = self.performances.get(portfolio_id)
        if not perf:
            logger.warning(f"Portfolio {portfolio_id} not found in leaderboard")
            return False
        
        if accuracy is not None:
            perf.accuracy = accuracy
        if roi is not None:
            perf.roi = roi
        if total_trades is not None:
            perf.total_trades = total_trades
        if winning_trades is not None:
            perf.winning_trades = winning_trades
        if total_value is not None:
            perf.total_value = total_value
        if profit_loss is not None:
            perf.profit_loss = profit_loss
        
        # Recalculate combined score
        perf.calculate_combined_score()
        perf.last_updated = datetime.now()
        
        self._save_performance(perf)
        logger.debug(f"Updated performance for portfolio {portfolio_id}")
        return True
    
    def get_leaderboard(
        self,
        category: LeaderboardCategory,
        top_n: int = 3,
        testnet_only: bool = True
    ) -> List[LeaderboardEntry]:
        """
        Get leaderboard for a specific category
        
        Args:
            category: Leaderboard category
            top_n: Number of top entries to return
            testnet_only: Only include testnet portfolios
            
        Returns:
            List of LeaderboardEntry objects
        """
        # Get all performances
        perfs = list(self.performances.values())
        
        # Filter by network if needed
        if testnet_only:
            # In production, check portfolio network status
            pass
        
        # Sort by category
        if category == LeaderboardCategory.ACCURACY:
            perfs.sort(key=lambda p: p.accuracy, reverse=True)
            score_key = 'accuracy'
        elif category == LeaderboardCategory.ROI:
            perfs.sort(key=lambda p: p.roi, reverse=True)
            score_key = 'roi'
        else:  # COMBINED
            perfs.sort(key=lambda p: p.combined_score, reverse=True)
            score_key = 'combined_score'
        
        # Create leaderboard entries
        entries = []
        for rank, perf in enumerate(perfs[:top_n], start=1):
            entry = LeaderboardEntry(
                rank=rank,
                portfolio_id=perf.portfolio_id,
                user_id=perf.user_id,
                username=perf.username,
                portfolio_name=perf.portfolio_name,
                score=getattr(perf, score_key),
                accuracy=perf.accuracy,
                roi=perf.roi,
                total_trades=perf.total_trades,
                is_testnet=testnet_only
            )
            entries.append(entry)
        
        return entries
    
    def get_all_leaderboards(
        self,
        top_n: int = 3,
        testnet_only: bool = True
    ) -> Dict[str, List[LeaderboardEntry]]:
        """
        Get all leaderboards
        
        Returns:
            Dictionary with category keys and leaderboard entries
        """
        leaderboards = {}
        
        for category in LeaderboardCategory:
            leaderboards[category.value] = self.get_leaderboard(
                category=category,
                top_n=top_n,
                testnet_only=testnet_only
            )
        
        return leaderboards
    
    def get_user_rankings(
        self,
        user_id: str,
        testnet_only: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get user's rankings across all categories
        
        Args:
            user_id: User ID
            testnet_only: Only consider testnet portfolios
            
        Returns:
            Dictionary with rankings per category
        """
        rankings = {}
        
        for category in LeaderboardCategory:
            # Get all performances sorted by category
            perfs = list(self.performances.values())
            
            if category == LeaderboardCategory.ACCURACY:
                perfs.sort(key=lambda p: p.accuracy, reverse=True)
            elif category == LeaderboardCategory.ROI:
                perfs.sort(key=lambda p: p.roi, reverse=True)
            else:  # COMBINED
                perfs.sort(key=lambda p: p.combined_score, reverse=True)
            
            # Find user's best portfolio in this category
            user_perfs = [p for p in perfs if p.user_id == user_id]
            
            if user_perfs:
                best_perf = user_perfs[0]
                rank = perfs.index(best_perf) + 1
                
                rankings[category.value] = {
                    'rank': rank,
                    'portfolio_id': best_perf.portfolio_id,
                    'portfolio_name': best_perf.portfolio_name,
                    'score': getattr(best_perf, 
                                    'accuracy' if category == LeaderboardCategory.ACCURACY 
                                    else 'roi' if category == LeaderboardCategory.ROI 
                                    else 'combined_score'),
                    'total_participants': len(perfs)
                }
        
        return rankings
    
    def get_leaderboard_summary(self, testnet_only: bool = True) -> Dict[str, Any]:
        """
        Get summary of leaderboard status
        
        Returns:
            Summary statistics
        """
        all_leaderboards = self.get_all_leaderboards(top_n=3, testnet_only=testnet_only)
        
        summary = {
            'total_portfolios': len(self.performances),
            'total_users': len(set(p.user_id for p in self.performances.values())),
            'leaderboards': {}
        }
        
        for category, entries in all_leaderboards.items():
            summary['leaderboards'][category] = {
                'top_3': [entry.to_dict() for entry in entries],
                'category_name': category.replace('_', ' ').title()
            }
        
        return summary
    
    def _save_performance(self, perf: PortfolioPerformance):
        """Save performance to disk"""
        filepath = self.performance_dir / f"{perf.portfolio_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(perf.to_dict(), f, indent=2)
    
    def _load_performances(self):
        """Load all performances from disk"""
        for filepath in self.performance_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                portfolio_id = data['portfolio_id']
                logger.debug(f"Loaded performance: {portfolio_id}")
                
            except Exception as e:
                logger.error(f"Error loading performance from {filepath}: {e}")
    
    def save_leaderboard_snapshot(self, testnet_only: bool = True):
        """Save current leaderboard state"""
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'leaderboards': {}
        }
        
        all_leaderboards = self.get_all_leaderboards(top_n=10, testnet_only=testnet_only)
        
        for category, entries in all_leaderboards.items():
            snapshot['leaderboards'][category] = [entry.to_dict() for entry in entries]
        
        filename = f"leaderboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.leaderboard_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        logger.info(f"Saved leaderboard snapshot to {filepath}")
