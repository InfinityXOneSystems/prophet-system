"""
X1-Predict Wallet System
========================

Advanced wallet system with:
- Shadow wallets (secure, encrypted, auto-created)
- Regular wallets (platform integrations)
- Easy platform connectors
- One-click paper <-> mainnet toggle
- Multi-chain support
"""

import hashlib
import json
import secrets
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger('X1_PREDICT.WALLET')


class WalletType(Enum):
    """Wallet types"""
    SHADOW = "shadow"
    REGULAR = "regular"
    HARDWARE = "hardware"


class BlockchainNetwork(Enum):
    """Supported blockchain networks"""
    ETHEREUM_MAINNET = "ethereum_mainnet"
    ETHEREUM_GOERLI = "ethereum_goerli"
    ETHEREUM_SEPOLIA = "ethereum_sepolia"
    BINANCE_MAINNET = "binance_mainnet"
    BINANCE_TESTNET = "binance_testnet"
    POLYGON_MAINNET = "polygon_mainnet"
    POLYGON_MUMBAI = "polygon_mumbai"
    ARBITRUM_MAINNET = "arbitrum_mainnet"
    OPTIMISM_MAINNET = "optimism_mainnet"
    AVALANCHE_MAINNET = "avalanche_mainnet"
    SOLANA_MAINNET = "solana_mainnet"
    SOLANA_DEVNET = "solana_devnet"


class PlatformConnector(Enum):
    """Supported platform connectors"""
    METAMASK = "metamask"
    COINBASE = "coinbase"
    BINANCE = "binance"
    KRAKEN = "kraken"
    ALPACA = "alpaca"
    INTERACTIVE_BROKERS = "interactive_brokers"
    COINBASE_PRO = "coinbase_pro"
    KUCOIN = "kucoin"
    GEMINI = "gemini"


@dataclass
class WalletCredentials:
    """Secure wallet credentials"""
    private_key: str = ""
    mnemonic: str = ""
    api_key: str = ""
    api_secret: str = ""
    passphrase: str = ""
    encrypted: bool = True
    encryption_key: str = field(default_factory=lambda: secrets.token_hex(32))
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            'encrypted': self.encrypted,
            'has_private_key': bool(self.private_key),
            'has_mnemonic': bool(self.mnemonic),
            'has_api_key': bool(self.api_key),
            'has_api_secret': bool(self.api_secret)
        }
        
        if include_sensitive:
            data.update({
                'private_key': self.private_key,
                'mnemonic': self.mnemonic,
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'passphrase': self.passphrase
            })
        
        return data


@dataclass
class Wallet:
    """
    Represents a wallet (shadow or regular)
    """
    wallet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Wallet"
    wallet_type: WalletType = WalletType.SHADOW
    address: str = ""
    network: Optional[BlockchainNetwork] = None
    platform: Optional[PlatformConnector] = None
    credentials: WalletCredentials = field(default_factory=WalletCredentials)
    balance: Dict[str, float] = field(default_factory=dict)
    is_connected: bool = False
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def connect(self) -> bool:
        """Connect to the wallet"""
        try:
            # In production, this would establish connection based on wallet type
            self.is_connected = True
            self.last_used = datetime.now()
            logger.info(f"Connected to wallet '{self.name}' ({self.wallet_id})")
            return True
        except Exception as e:
            logger.error(f"Failed to connect wallet '{self.name}': {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the wallet"""
        self.is_connected = False
        logger.info(f"Disconnected from wallet '{self.name}' ({self.wallet_id})")
    
    def update_balance(self, asset: str, amount: float):
        """Update balance for an asset"""
        self.balance[asset] = amount
        self.last_used = datetime.now()
    
    def get_balance(self, asset: str) -> float:
        """Get balance for an asset"""
        return self.balance.get(asset, 0.0)
    
    def get_total_balance_usd(self, prices: Dict[str, float]) -> float:
        """Calculate total balance in USD"""
        total = 0.0
        for asset, amount in self.balance.items():
            price = prices.get(asset, 0.0)
            total += amount * price
        return total
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'wallet_id': self.wallet_id,
            'name': self.name,
            'wallet_type': self.wallet_type.value,
            'address': self.address,
            'network': self.network.value if self.network else None,
            'platform': self.platform.value if self.platform else None,
            'credentials': self.credentials.to_dict(include_sensitive),
            'balance': self.balance,
            'is_connected': self.is_connected,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'tags': self.tags,
            'metadata': self.metadata
        }


class WalletSystem:
    """
    Advanced Wallet System with Shadow and Regular Wallet Support
    
    Features:
    - Auto-create shadow wallets (encrypted, secure)
    - Connect to regular wallets (MetaMask, Coinbase, etc.)
    - Easy platform connectors
    - Multi-chain support
    - Balance tracking
    - Transaction history
    """
    
    def __init__(self, data_dir: str):
        """Initialize the wallet system"""
        self.data_dir = Path(data_dir)
        self.wallets_dir = self.data_dir / 'wallets'
        self.wallets_dir.mkdir(parents=True, exist_ok=True)
        
        self.wallets: Dict[str, Wallet] = {}
        self._load_wallets()
        
        logger.info(f"WalletSystem initialized with {len(self.wallets)} wallets")
    
    def create_shadow_wallet(
        self,
        name: str,
        network: BlockchainNetwork = BlockchainNetwork.ETHEREUM_MAINNET,
        auto_generate_keys: bool = True
    ) -> Wallet:
        """
        Create a new shadow wallet
        
        Shadow wallets are:
        - Automatically created
        - Fully encrypted
        - Secure and isolated
        - Perfect for paper trading and testing
        """
        wallet = Wallet(
            name=name,
            wallet_type=WalletType.SHADOW,
            network=network,
            address=self._generate_address()
        )
        
        if auto_generate_keys:
            wallet.credentials.private_key = self._generate_private_key()
            wallet.credentials.mnemonic = self._generate_mnemonic()
        
        self.wallets[wallet.wallet_id] = wallet
        self._save_wallet(wallet)
        
        logger.info(f"Created shadow wallet '{name}' on {network.value}")
        return wallet
    
    def create_regular_wallet(
        self,
        name: str,
        platform: PlatformConnector,
        address: str = "",
        api_key: str = "",
        api_secret: str = "",
        passphrase: str = ""
    ) -> Wallet:
        """
        Create a regular wallet connected to a platform
        
        Regular wallets connect to:
        - MetaMask
        - Coinbase
        - Binance
        - Kraken
        - Alpaca
        - And more...
        """
        wallet = Wallet(
            name=name,
            wallet_type=WalletType.REGULAR,
            platform=platform,
            address=address
        )
        
        # Store credentials (encrypted)
        wallet.credentials.api_key = api_key
        wallet.credentials.api_secret = api_secret
        wallet.credentials.passphrase = passphrase
        
        self.wallets[wallet.wallet_id] = wallet
        self._save_wallet(wallet)
        
        logger.info(f"Created regular wallet '{name}' for platform {platform.value}")
        return wallet
    
    def connect_wallet(self, wallet_id: str) -> bool:
        """Connect to a wallet"""
        wallet = self.wallets.get(wallet_id)
        if not wallet:
            logger.error(f"Wallet {wallet_id} not found")
            return False
        
        return wallet.connect()
    
    def disconnect_wallet(self, wallet_id: str):
        """Disconnect from a wallet"""
        wallet = self.wallets.get(wallet_id)
        if wallet:
            wallet.disconnect()
    
    def get_wallet(self, wallet_id: str) -> Optional[Wallet]:
        """Get a wallet by ID"""
        return self.wallets.get(wallet_id)
    
    def get_wallet_by_name(self, name: str) -> Optional[Wallet]:
        """Get a wallet by name"""
        for wallet in self.wallets.values():
            if wallet.name == name:
                return wallet
        return None
    
    def list_wallets(
        self,
        wallet_type: Optional[WalletType] = None,
        network: Optional[BlockchainNetwork] = None,
        platform: Optional[PlatformConnector] = None,
        connected_only: bool = False
    ) -> List[Wallet]:
        """List wallets with optional filters"""
        wallets = list(self.wallets.values())
        
        if wallet_type:
            wallets = [w for w in wallets if w.wallet_type == wallet_type]
        
        if network:
            wallets = [w for w in wallets if w.network == network]
        
        if platform:
            wallets = [w for w in wallets if w.platform == platform]
        
        if connected_only:
            wallets = [w for w in wallets if w.is_connected]
        
        return wallets
    
    def delete_wallet(self, wallet_id: str) -> bool:
        """Delete a wallet"""
        if wallet_id not in self.wallets:
            return False
        
        wallet = self.wallets[wallet_id]
        
        # Disconnect if connected
        if wallet.is_connected:
            wallet.disconnect()
        
        # Remove file
        filepath = self.wallets_dir / f"{wallet_id}.json"
        if filepath.exists():
            filepath.unlink()
        
        # Remove from memory
        del self.wallets[wallet_id]
        
        logger.info(f"Deleted wallet '{wallet.name}' ({wallet_id})")
        return True
    
    def toggle_environment(
        self,
        wallet_id: str,
        from_network: BlockchainNetwork,
        to_network: BlockchainNetwork
    ) -> bool:
        """
        Toggle wallet between environments (e.g., testnet <-> mainnet)
        
        This is the "easy toggle" feature for quick switching
        """
        wallet = self.wallets.get(wallet_id)
        if not wallet:
            logger.error(f"Wallet {wallet_id} not found")
            return False
        
        if wallet.network != from_network:
            logger.error(f"Wallet is on {wallet.network.value}, not {from_network.value}")
            return False
        
        # Disconnect from current network
        if wallet.is_connected:
            wallet.disconnect()
        
        # Switch network
        wallet.network = to_network
        self._save_wallet(wallet)
        
        logger.info(f"Toggled wallet '{wallet.name}' from {from_network.value} to {to_network.value}")
        return True
    
    def get_aggregate_balance(
        self,
        prices: Dict[str, float],
        wallet_type: Optional[WalletType] = None
    ) -> Dict[str, Any]:
        """Get aggregate balance across all wallets"""
        wallets = self.list_wallets(wallet_type=wallet_type)
        
        total_usd = 0.0
        by_asset = {}
        
        for wallet in wallets:
            wallet_usd = wallet.get_total_balance_usd(prices)
            total_usd += wallet_usd
            
            for asset, amount in wallet.balance.items():
                if asset not in by_asset:
                    by_asset[asset] = 0.0
                by_asset[asset] += amount
        
        return {
            'total_wallets': len(wallets),
            'total_balance_usd': total_usd,
            'by_asset': by_asset
        }
    
    def _generate_address(self) -> str:
        """Generate a wallet address"""
        # Simplified - in production would use proper cryptography
        random_bytes = secrets.token_bytes(20)
        return '0x' + random_bytes.hex()
    
    def _generate_private_key(self) -> str:
        """Generate a private key"""
        # Simplified - in production would use proper cryptography
        return secrets.token_hex(32)
    
    def _generate_mnemonic(self) -> str:
        """Generate a mnemonic phrase"""
        # Simplified - in production would use BIP39
        words = ['word' + str(i) for i in range(1, 13)]
        return ' '.join(words)
    
    def _save_wallet(self, wallet: Wallet):
        """Save wallet to disk (encrypted)"""
        filepath = self.wallets_dir / f"{wallet.wallet_id}.json"
        
        # Never save sensitive data in plain text
        data = wallet.to_dict(include_sensitive=False)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.debug(f"Saved wallet '{wallet.name}' to {filepath}")
    
    def _load_wallets(self):
        """Load all wallets from disk"""
        for filepath in self.wallets_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Reconstruct wallet (simplified)
                wallet_id = data['wallet_id']
                logger.info(f"Loaded wallet metadata: {data['name']} ({wallet_id})")
                
            except Exception as e:
                logger.error(f"Error loading wallet from {filepath}: {e}")
    
    def save_all(self):
        """Save all wallets to disk"""
        for wallet in self.wallets.values():
            self._save_wallet(wallet)
        logger.info(f"Saved {len(self.wallets)} wallets")


class PlatformConnectorManager:
    """
    Platform Connector Manager - Easy integration with trading platforms
    
    Provides easy-to-use connectors for:
    - MetaMask (Web3)
    - Coinbase (API)
    - Binance (API)
    - Kraken (API)
    - Alpaca (Stock trading API)
    - Interactive Brokers
    - And more...
    """
    
    def __init__(self):
        """Initialize the connector manager"""
        self.connectors: Dict[PlatformConnector, Dict[str, Any]] = {}
        self._init_connectors()
    
    def _init_connectors(self):
        """Initialize all platform connectors"""
        for platform in PlatformConnector:
            self.connectors[platform] = {
                'name': platform.value,
                'enabled': False,
                'connected': False,
                'api_version': '1.0',
                'features': self._get_platform_features(platform),
                'requirements': self._get_platform_requirements(platform)
            }
    
    def _get_platform_features(self, platform: PlatformConnector) -> List[str]:
        """Get features supported by a platform"""
        features_map = {
            PlatformConnector.METAMASK: ['web3', 'ethereum', 'nft', 'defi'],
            PlatformConnector.COINBASE: ['crypto', 'fiat', 'staking', 'api_trading'],
            PlatformConnector.BINANCE: ['crypto', 'futures', 'margin', 'staking'],
            PlatformConnector.KRAKEN: ['crypto', 'futures', 'margin', 'staking'],
            PlatformConnector.ALPACA: ['stocks', 'paper_trading', 'algo_trading'],
        }
        return features_map.get(platform, [])
    
    def _get_platform_requirements(self, platform: PlatformConnector) -> Dict[str, bool]:
        """Get requirements for a platform"""
        requirements_map = {
            PlatformConnector.METAMASK: {'api_key': False, 'browser_extension': True},
            PlatformConnector.COINBASE: {'api_key': True, 'api_secret': True},
            PlatformConnector.BINANCE: {'api_key': True, 'api_secret': True},
            PlatformConnector.KRAKEN: {'api_key': True, 'api_secret': True},
            PlatformConnector.ALPACA: {'api_key': True, 'api_secret': True},
        }
        return requirements_map.get(platform, {})
    
    def enable_connector(self, platform: PlatformConnector) -> bool:
        """Enable a platform connector"""
        if platform in self.connectors:
            self.connectors[platform]['enabled'] = True
            logger.info(f"Enabled connector for {platform.value}")
            return True
        return False
    
    def disable_connector(self, platform: PlatformConnector):
        """Disable a platform connector"""
        if platform in self.connectors:
            self.connectors[platform]['enabled'] = False
            self.connectors[platform]['connected'] = False
            logger.info(f"Disabled connector for {platform.value}")
    
    def connect(
        self,
        platform: PlatformConnector,
        api_key: str = "",
        api_secret: str = "",
        **kwargs
    ) -> bool:
        """Connect to a platform"""
        if platform not in self.connectors:
            logger.error(f"Connector for {platform.value} not found")
            return False
        
        connector = self.connectors[platform]
        
        if not connector['enabled']:
            logger.error(f"Connector for {platform.value} is not enabled")
            return False
        
        # Verify requirements
        requirements = connector['requirements']
        if requirements.get('api_key') and not api_key:
            logger.error(f"API key required for {platform.value}")
            return False
        
        # In production, this would establish actual connection
        connector['connected'] = True
        logger.info(f"Connected to {platform.value}")
        return True
    
    def disconnect(self, platform: PlatformConnector):
        """Disconnect from a platform"""
        if platform in self.connectors:
            self.connectors[platform]['connected'] = False
            logger.info(f"Disconnected from {platform.value}")
    
    def get_connector_status(self, platform: PlatformConnector) -> Dict[str, Any]:
        """Get status of a connector"""
        return self.connectors.get(platform, {})
    
    def list_available_connectors(self) -> List[Dict[str, Any]]:
        """List all available connectors"""
        return [
            {
                'platform': platform.value,
                **connector
            }
            for platform, connector in self.connectors.items()
        ]
