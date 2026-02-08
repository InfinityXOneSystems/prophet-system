#!/usr/bin/env python3
"""
Gamification System Demo
========================

Interactive demo of the leaderboard and Infinity Coin system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.features.gamification_manager import GamificationManager


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("  X1-PREDICT GAMIFICATION SYSTEM")
    print("  Leaderboard Competition & Infinity Coin")
    print("="*60 + "\n")


def print_leaderboards(leaderboards_data):
    """Print leaderboards"""
    print("\n" + "="*60)
    print("  LEADERBOARDS - TOP 3 PERFORMERS")
    print("="*60)
    
    for category, data in leaderboards_data['leaderboards'].items():
        print(f"\n🏆 {data['category_name']}")
        print("-" * 60)
        
        if not data['entries']:
            print("  No entries yet. Be the first to compete!")
            continue
        
        for entry in data['entries']:
            print(f"  #{entry['rank']} {entry['username']} - {entry['portfolio_name']}")
            print(f"      Score: {entry['score']:.2f} | Accuracy: {entry['accuracy']:.2f}% | ROI: {entry['roi']:.2f}%")
            print(f"      Trades: {entry['total_trades']}")
    
    print("\n" + "="*60)


def demo_user_registration(manager: GamificationManager):
    """Demo user registration"""
    print("\n📝 USER REGISTRATION DEMO")
    print("-" * 60)
    
    # Register demo users
    users = [
        ("trader_alice", "password123", "alice@example.com"),
        ("crypto_bob", "password123", "bob@example.com"),
        ("investor_charlie", "password123", "charlie@example.com")
    ]
    
    sessions = {}
    
    for username, password, email in users:
        result = manager.register_and_login(username, password, email)
        if result['success']:
            sessions[username] = result['session_id']
            print(f"✓ Registered: {username}")
        else:
            # Try login if already registered
            login_result = manager.login(username, password)
            if login_result['success']:
                sessions[username] = login_result['session_id']
                print(f"✓ Logged in: {username} (existing user)")
    
    return sessions


def demo_portfolio_registration(manager: GamificationManager, sessions):
    """Demo portfolio registration"""
    print("\n💼 PORTFOLIO REGISTRATION DEMO")
    print("-" * 60)
    
    portfolios = [
        ("trader_alice", "Alice's Alpha Strategy"),
        ("crypto_bob", "Bob's Crypto Portfolio"),
        ("investor_charlie", "Charlie's Conservative Fund")
    ]
    
    portfolio_ids = {}
    
    for username, portfolio_name in portfolios:
        import uuid
        portfolio_id = str(uuid.uuid4())
        
        if username in sessions:
            result = manager.register_portfolio_for_competition(
                session_id=sessions[username],
                portfolio_id=portfolio_id,
                portfolio_name=portfolio_name
            )
            
            if result['success']:
                portfolio_ids[username] = portfolio_id
                print(f"✓ Registered: {portfolio_name}")
        else:
            print(f"✗ Skipped {username} (not logged in)")
    
    return portfolio_ids


def demo_update_performance(manager: GamificationManager, portfolio_ids):
    """Demo performance updates"""
    print("\n📈 PERFORMANCE UPDATE DEMO")
    print("-" * 60)
    
    # Simulate performance data
    performances = [
        ("trader_alice", 75.5, 42.3, 150, 110),
        ("crypto_bob", 82.1, 35.8, 200, 165),
        ("investor_charlie", 68.9, 55.2, 100, 70)
    ]
    
    for username, accuracy, roi, total_trades, winning_trades in performances:
        if username in portfolio_ids:
            portfolio_id = portfolio_ids[username]
            
            manager.update_portfolio_performance(
                portfolio_id=portfolio_id,
                accuracy=accuracy,
                roi=roi,
                total_trades=total_trades,
                winning_trades=winning_trades
            )
            
            print(f"✓ Updated {username}: Accuracy={accuracy}%, ROI={roi}%")


def demo_infinity_coin(manager: GamificationManager, sessions):
    """Demo Infinity Coin deployment"""
    print("\n🪙 INFINITY COIN DEPLOYMENT DEMO")
    print("-" * 60)
    
    # Get Infinity Coin config
    config = manager.infinity_coin_deployer.get_infinity_coin_config()
    
    print(f"Token Name: {config['name']}")
    print(f"Symbol: {config['symbol']}")
    print(f"Initial Supply: {config['initial_supply']:,}")
    print(f"Max Supply: {config['max_supply']:,}")
    print(f"Features: {', '.join(config['features'])}")
    
    # Deploy to testnet
    username = "trader_alice"
    if username in sessions:
        print(f"\n🚀 Deploying to Ethereum Goerli testnet...")
        result = manager.deploy_infinity_coin(
            session_id=sessions[username],
            network="ethereum_goerli"
        )
        
        if result['success']:
            deployment = result['deployment']
            print(f"✓ Deployment successful!")
            print(f"  Contract Address: {deployment['contract_address']}")
            print(f"  Transaction: {deployment['deployment_tx']}")
            print(f"  Explorer: {result['explorer_url']}")


def main():
    """Main demo function"""
    print_banner()
    
    # Initialize manager
    print("Initializing Gamification System...")
    manager = GamificationManager('data')
    print("✓ System ready!\n")
    
    # Run demos
    sessions = demo_user_registration(manager)
    
    if not sessions:
        print("\n❌ No users available. Cannot continue demo.")
        return
    
    portfolio_ids = demo_portfolio_registration(manager, sessions)
    demo_update_performance(manager, portfolio_ids)
    
    # Display leaderboards
    leaderboards = manager.get_leaderboards(top_n=3)
    print_leaderboards(leaderboards)
    
    # Infinity Coin demo
    demo_infinity_coin(manager, sessions)
    
    # Display dashboard data
    print("\n📊 DASHBOARD DATA")
    print("-" * 60)
    dashboard = manager.get_dashboard_data()
    print(f"Total Portfolios: {dashboard['leaderboard_summary']['total_portfolios']}")
    print(f"Total Users: {dashboard['leaderboard_summary']['total_users']}")
    
    print("\n✨ Demo complete! System is ready for use.")
    print("\nTo use the system:")
    print("  1. Register/login users via GamificationManager")
    print("  2. Register portfolios for competition")
    print("  3. Update performance metrics")
    print("  4. View leaderboards in real-time")
    print("  5. Deploy Infinity Coin to testnet")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
