"""
Gamification Manager
====================

Central manager for leaderboard gamification system.
Integrates user authentication, leaderboards, and portfolio tracking.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.auth.user_authentication import UserAuthenticationSystem, User, Session
from src.features.leaderboard_system import LeaderboardSystem, LeaderboardCategory
from src.features.infinity_coin_deployer import InfinityCoinDeployer, Network

logger = logging.getLogger('X1_PREDICT.GAMIFICATION')


class GamificationManager:
    """
    Gamification Manager
    
    Central system for managing:
    - User authentication
    - Leaderboard competitions
    - Portfolio performance tracking
    - Infinity Coin integration
    """
    
    def __init__(self, data_dir: str):
        """Initialize gamification manager"""
        self.data_dir = Path(data_dir)
        
        # Initialize subsystems
        self.auth_system = UserAuthenticationSystem(str(self.data_dir))
        self.leaderboard_system = LeaderboardSystem(str(self.data_dir))
        self.infinity_coin_deployer = InfinityCoinDeployer(str(self.data_dir))
        
        logger.info("GamificationManager initialized")
    
    def register_and_login(
        self,
        username: str,
        password: str,
        email: str
    ) -> Dict[str, Any]:
        """
        Register new user and log them in
        
        Args:
            username: Username
            password: Password
            email: Email
            
        Returns:
            Login result with session
        """
        # Register user
        user = self.auth_system.register_user(username, password, email)
        
        if not user:
            return {
                'success': False,
                'error': 'Registration failed - username may already exist'
            }
        
        # Auto-login
        session = self.auth_system.login(username, password)
        
        if not session:
            return {
                'success': False,
                'error': 'Login failed after registration'
            }
        
        return {
            'success': True,
            'user': user.to_dict(),
            'session_id': session.session_id,
            'message': f'Welcome {username}! Your account has been created.'
        }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login user
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Login result with session
        """
        session = self.auth_system.login(username, password)
        
        if not session:
            return {
                'success': False,
                'error': 'Invalid username or password'
            }
        
        user = self.auth_system.verify_session(session.session_id)
        
        return {
            'success': True,
            'user': user.to_dict(),
            'session_id': session.session_id,
            'message': f'Welcome back {username}!'
        }
    
    def register_portfolio_for_competition(
        self,
        session_id: str,
        portfolio_id: str,
        portfolio_name: str
    ) -> Dict[str, Any]:
        """
        Register a portfolio for leaderboard competition
        
        Args:
            session_id: User session ID
            portfolio_id: Portfolio ID
            portfolio_name: Portfolio name
            
        Returns:
            Registration result
        """
        # Verify session
        user = self.auth_system.verify_session(session_id)
        if not user:
            return {
                'success': False,
                'error': 'Invalid session'
            }
        
        # Register portfolio
        perf = self.leaderboard_system.register_portfolio(
            portfolio_id=portfolio_id,
            user_id=user.user_id,
            username=user.username,
            portfolio_name=portfolio_name
        )
        
        logger.info(f"Registered portfolio {portfolio_name} for user {user.username}")
        
        return {
            'success': True,
            'portfolio_id': portfolio_id,
            'message': f'Portfolio "{portfolio_name}" registered for competition!'
        }
    
    def update_portfolio_performance(
        self,
        portfolio_id: str,
        accuracy: float = None,
        roi: float = None,
        total_trades: int = None,
        winning_trades: int = None
    ) -> bool:
        """Update portfolio performance in leaderboard"""
        return self.leaderboard_system.update_performance(
            portfolio_id=portfolio_id,
            accuracy=accuracy,
            roi=roi,
            total_trades=total_trades,
            winning_trades=winning_trades
        )
    
    def get_leaderboards(
        self,
        session_id: str = None,
        top_n: int = 3
    ) -> Dict[str, Any]:
        """
        Get all leaderboards
        
        Args:
            session_id: User session ID (optional)
            top_n: Number of top entries
            
        Returns:
            Leaderboard data
        """
        user = None
        if session_id:
            user = self.auth_system.verify_session(session_id)
        
        # Get all leaderboards
        leaderboards = self.leaderboard_system.get_all_leaderboards(top_n=top_n)
        
        result = {
            'leaderboards': {},
            'user_rankings': None
        }
        
        # Format leaderboards
        for category, entries in leaderboards.items():
            result['leaderboards'][category] = {
                'category_name': category.replace('_', ' ').title(),
                'entries': [entry.to_dict() for entry in entries]
            }
        
        # Add user rankings if logged in
        if user:
            result['user_rankings'] = self.leaderboard_system.get_user_rankings(user.user_id)
        
        return result
    
    def get_user_profile(self, session_id: str) -> Dict[str, Any]:
        """
        Get user profile with competition stats
        
        Args:
            session_id: User session ID
            
        Returns:
            User profile data
        """
        user = self.auth_system.verify_session(session_id)
        
        if not user:
            return {
                'success': False,
                'error': 'Invalid session'
            }
        
        # Get user rankings
        rankings = self.leaderboard_system.get_user_rankings(user.user_id)
        
        return {
            'success': True,
            'user': user.to_dict(),
            'rankings': rankings,
            'infinity_coin_info': self.infinity_coin_deployer.get_infinity_coin_config()
        }
    
    def deploy_infinity_coin(
        self,
        session_id: str,
        network: str = "ethereum_goerli"
    ) -> Dict[str, Any]:
        """
        Deploy Infinity Coin to testnet
        
        Args:
            session_id: User session ID
            network: Target network
            
        Returns:
            Deployment result
        """
        user = self.auth_system.verify_session(session_id)
        
        if not user:
            return {
                'success': False,
                'error': 'Invalid session'
            }
        
        # Deploy to testnet
        network_enum = Network(network)
        result = self.infinity_coin_deployer.deploy_to_testnet(
            network=network_enum,
            deployer_address=f"0x{user.user_id[:40]}"  # Simulated address
        )
        
        return result
    
    def get_dashboard_data(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get complete dashboard data
        
        Args:
            session_id: User session ID (optional)
            
        Returns:
            Dashboard data with leaderboards and user info
        """
        data = {
            'leaderboards': self.get_leaderboards(session_id, top_n=3),
            'leaderboard_summary': self.leaderboard_system.get_leaderboard_summary(),
            'infinity_coin': self.infinity_coin_deployer.get_infinity_coin_config()
        }
        
        if session_id:
            user = self.auth_system.verify_session(session_id)
            if user:
                data['user'] = user.to_dict()
                data['user_rankings'] = self.leaderboard_system.get_user_rankings(user.user_id)
        
        return data
