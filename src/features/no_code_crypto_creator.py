"""
X1-Predict No-Code Crypto Creation System
=========================================

User-friendly no-code system for creating cryptocurrencies and tokens:
- ERC-20 token creation
- NFT collection deployment
- DeFi protocol templates
- Smart contract wizard
- One-click deployment
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger('X1_PREDICT.NO_CODE_CRYPTO')


class TokenStandard(Enum):
    """Supported token standards"""
    ERC20 = "erc20"
    ERC721 = "erc721"  # NFT
    ERC1155 = "erc1155"  # Multi-token
    BEP20 = "bep20"  # Binance
    SPL = "spl"  # Solana


class TokenFeature(Enum):
    """Token features that can be enabled"""
    MINTABLE = "mintable"
    BURNABLE = "burnable"
    PAUSABLE = "pausable"
    SNAPSHOT = "snapshot"
    VOTES = "votes"
    FLASH_MINTING = "flash_minting"
    PERMIT = "permit"
    CAPPED = "capped"


class DeploymentStatus(Enum):
    """Deployment status"""
    DRAFT = "draft"
    VALIDATING = "validating"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"


@dataclass
class TokenomicsConfig:
    """Tokenomics configuration"""
    total_supply: float = 1000000.0
    initial_supply: float = 1000000.0
    max_supply: Optional[float] = None
    decimals: int = 18
    
    # Distribution
    team_allocation_pct: float = 15.0
    public_sale_pct: float = 50.0
    liquidity_pct: float = 20.0
    marketing_pct: float = 10.0
    reserve_pct: float = 5.0
    
    # Vesting
    team_vesting_months: int = 24
    team_cliff_months: int = 6
    
    def validate(self) -> bool:
        """Validate tokenomics configuration"""
        total_pct = (
            self.team_allocation_pct +
            self.public_sale_pct +
            self.liquidity_pct +
            self.marketing_pct +
            self.reserve_pct
        )
        
        if abs(total_pct - 100.0) > 0.01:
            logger.error(f"Total allocation must be 100%, got {total_pct}%")
            return False
        
        if self.max_supply and self.initial_supply > self.max_supply:
            logger.error("Initial supply cannot exceed max supply")
            return False
        
        return True


@dataclass
class SmartContractTemplate:
    """Smart contract template"""
    template_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Token Template"
    description: str = ""
    standard: TokenStandard = TokenStandard.ERC20
    features: List[TokenFeature] = field(default_factory=list)
    code_template: str = ""
    constructor_params: List[str] = field(default_factory=list)
    is_audited: bool = False
    audit_report_url: str = ""
    gas_estimate: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'template_id': self.template_id,
            'name': self.name,
            'description': self.description,
            'standard': self.standard.value,
            'features': [f.value for f in self.features],
            'constructor_params': self.constructor_params,
            'is_audited': self.is_audited,
            'audit_report_url': self.audit_report_url,
            'gas_estimate': self.gas_estimate
        }


@dataclass
class CryptoProject:
    """Represents a crypto project created via no-code system"""
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "My Token"
    symbol: str = "MTK"
    description: str = ""
    website: str = ""
    whitepaper_url: str = ""
    
    # Technical details
    standard: TokenStandard = TokenStandard.ERC20
    features: List[TokenFeature] = field(default_factory=list)
    tokenomics: TokenomicsConfig = field(default_factory=TokenomicsConfig)
    
    # Deployment
    network: str = "ethereum_goerli"  # Default to testnet
    contract_address: str = ""
    deployer_address: str = ""
    deployment_tx: str = ""
    deployment_date: Optional[datetime] = None
    status: DeploymentStatus = DeploymentStatus.DRAFT
    
    # Metadata
    logo_url: str = ""
    social_links: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def validate(self) -> bool:
        """Validate project configuration"""
        # Validate name and symbol
        if not self.name or len(self.name) < 3:
            logger.error("Name must be at least 3 characters")
            return False
        
        if not self.symbol or len(self.symbol) < 2:
            logger.error("Symbol must be at least 2 characters")
            return False
        
        # Validate tokenomics
        if not self.tokenomics.validate():
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'project_id': self.project_id,
            'name': self.name,
            'symbol': self.symbol,
            'description': self.description,
            'website': self.website,
            'whitepaper_url': self.whitepaper_url,
            'standard': self.standard.value,
            'features': [f.value for f in self.features],
            'tokenomics': asdict(self.tokenomics),
            'network': self.network,
            'contract_address': self.contract_address,
            'deployer_address': self.deployer_address,
            'deployment_tx': self.deployment_tx,
            'deployment_date': self.deployment_date.isoformat() if self.deployment_date else None,
            'status': self.status.value,
            'logo_url': self.logo_url,
            'social_links': self.social_links,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class NoCodeCryptoCreator:
    """
    No-Code Cryptocurrency Creation System
    
    Features:
    - Wizard-based token creation
    - Pre-built smart contract templates
    - ERC-20, ERC-721, ERC-1155 support
    - Tokenomics configuration
    - One-click deployment
    - Testnet and mainnet support
    """
    
    def __init__(self, data_dir: str):
        """Initialize the no-code crypto creator"""
        self.data_dir = Path(data_dir)
        self.projects_dir = self.data_dir / 'crypto_projects'
        self.templates_dir = self.data_dir / 'contract_templates'
        
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        self.projects: Dict[str, CryptoProject] = {}
        self.templates: Dict[str, SmartContractTemplate] = {}
        
        self._init_templates()
        self._load_projects()
        
        logger.info(f"NoCodeCryptoCreator initialized with {len(self.projects)} projects")
    
    def _init_templates(self):
        """Initialize smart contract templates"""
        # ERC-20 Basic Template
        erc20_basic = SmartContractTemplate(
            name="ERC-20 Basic Token",
            description="Standard ERC-20 token with basic functionality",
            standard=TokenStandard.ERC20,
            features=[],
            constructor_params=["name", "symbol", "initialSupply"],
            is_audited=True,
            gas_estimate=1500000
        )
        self.templates[erc20_basic.template_id] = erc20_basic
        
        # ERC-20 Advanced Template
        erc20_advanced = SmartContractTemplate(
            name="ERC-20 Advanced Token",
            description="Advanced ERC-20 with minting, burning, and pausable features",
            standard=TokenStandard.ERC20,
            features=[
                TokenFeature.MINTABLE,
                TokenFeature.BURNABLE,
                TokenFeature.PAUSABLE
            ],
            constructor_params=["name", "symbol", "initialSupply"],
            is_audited=True,
            gas_estimate=2500000
        )
        self.templates[erc20_advanced.template_id] = erc20_advanced
        
        # NFT Template
        erc721_template = SmartContractTemplate(
            name="ERC-721 NFT Collection",
            description="Standard NFT collection with minting and metadata",
            standard=TokenStandard.ERC721,
            features=[TokenFeature.MINTABLE, TokenFeature.BURNABLE],
            constructor_params=["name", "symbol", "baseURI"],
            is_audited=True,
            gas_estimate=3000000
        )
        self.templates[erc721_template.template_id] = erc721_template
        
        logger.info(f"Initialized {len(self.templates)} contract templates")
    
    def create_project(
        self,
        name: str,
        symbol: str,
        description: str = "",
        standard: TokenStandard = TokenStandard.ERC20,
        initial_supply: float = 1000000.0
    ) -> CryptoProject:
        """
        Create a new crypto project
        
        This is the wizard's first step - basic project setup
        """
        project = CryptoProject(
            name=name,
            symbol=symbol.upper(),
            description=description,
            standard=standard
        )
        
        project.tokenomics.total_supply = initial_supply
        project.tokenomics.initial_supply = initial_supply
        
        self.projects[project.project_id] = project
        self._save_project(project)
        
        logger.info(f"Created crypto project '{name}' ({symbol})")
        return project
    
    def configure_tokenomics(
        self,
        project_id: str,
        tokenomics: TokenomicsConfig
    ) -> bool:
        """
        Configure tokenomics for a project
        
        This is the wizard's second step - tokenomics setup
        """
        project = self.projects.get(project_id)
        if not project:
            logger.error(f"Project {project_id} not found")
            return False
        
        if not tokenomics.validate():
            return False
        
        project.tokenomics = tokenomics
        project.updated_at = datetime.now()
        self._save_project(project)
        
        logger.info(f"Configured tokenomics for project '{project.name}'")
        return True
    
    def add_features(
        self,
        project_id: str,
        features: List[TokenFeature]
    ) -> bool:
        """
        Add features to a project
        
        This is the wizard's third step - feature selection
        """
        project = self.projects.get(project_id)
        if not project:
            logger.error(f"Project {project_id} not found")
            return False
        
        project.features = features
        project.updated_at = datetime.now()
        self._save_project(project)
        
        logger.info(f"Added {len(features)} features to project '{project.name}'")
        return True
    
    def validate_project(self, project_id: str) -> Dict[str, Any]:
        """
        Validate a project before deployment
        
        Returns validation results
        """
        project = self.projects.get(project_id)
        if not project:
            return {
                'valid': False,
                'errors': ['Project not found']
            }
        
        errors = []
        warnings = []
        
        # Validate basic info
        if not project.validate():
            errors.append("Project validation failed")
        
        # Check for common issues
        if project.tokenomics.total_supply > 1e12:
            warnings.append("Very high total supply - consider reducing")
        
        if not project.features:
            warnings.append("No features selected - consider adding useful features")
        
        if project.network.endswith('_mainnet'):
            warnings.append("Deploying to mainnet - double check all settings")
        
        project.status = DeploymentStatus.VALIDATING
        project.updated_at = datetime.now()
        self._save_project(project)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'gas_estimate': self._estimate_gas(project),
            'deployment_cost_eth': self._estimate_deployment_cost(project)
        }
    
    def deploy_project(
        self,
        project_id: str,
        deployer_address: str,
        network: str = "ethereum_goerli"
    ) -> Dict[str, Any]:
        """
        Deploy a project to blockchain
        
        This is the final step - one-click deployment
        """
        project = self.projects.get(project_id)
        if not project:
            return {
                'success': False,
                'error': 'Project not found'
            }
        
        # Validate first
        validation = self.validate_project(project_id)
        if not validation['valid']:
            return {
                'success': False,
                'error': 'Project validation failed',
                'validation': validation
            }
        
        # Update project
        project.network = network
        project.deployer_address = deployer_address
        project.status = DeploymentStatus.DEPLOYING
        project.updated_at = datetime.now()
        self._save_project(project)
        
        # In production, this would:
        # 1. Generate smart contract code from template
        # 2. Compile contract
        # 3. Deploy to blockchain
        # 4. Verify contract on explorer
        # 5. Update project with contract address
        
        # Simulated deployment
        project.contract_address = self._generate_contract_address()
        project.deployment_tx = self._generate_tx_hash()
        project.deployment_date = datetime.now()
        project.status = DeploymentStatus.DEPLOYED
        project.updated_at = datetime.now()
        self._save_project(project)
        
        logger.info(f"Deployed project '{project.name}' to {network}")
        
        return {
            'success': True,
            'project_id': project.project_id,
            'contract_address': project.contract_address,
            'deployment_tx': project.deployment_tx,
            'network': network,
            'explorer_url': self._get_explorer_url(network, project.contract_address)
        }
    
    def get_project(self, project_id: str) -> Optional[CryptoProject]:
        """Get a project by ID"""
        return self.projects.get(project_id)
    
    def list_projects(
        self,
        status: Optional[DeploymentStatus] = None,
        network: Optional[str] = None
    ) -> List[CryptoProject]:
        """List projects with optional filters"""
        projects = list(self.projects.values())
        
        if status:
            projects = [p for p in projects if p.status == status]
        
        if network:
            projects = [p for p in projects if p.network == network]
        
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        
        # Remove file
        filepath = self.projects_dir / f"{project_id}.json"
        if filepath.exists():
            filepath.unlink()
        
        # Remove from memory
        del self.projects[project_id]
        
        logger.info(f"Deleted project '{project.name}' ({project_id})")
        return True
    
    def list_templates(self, standard: Optional[TokenStandard] = None) -> List[SmartContractTemplate]:
        """List available templates"""
        templates = list(self.templates.values())
        
        if standard:
            templates = [t for t in templates if t.standard == standard]
        
        return templates
    
    def _estimate_gas(self, project: CryptoProject) -> int:
        """Estimate gas cost for deployment"""
        base_gas = 1500000
        
        # Add gas for each feature
        for feature in project.features:
            base_gas += 200000
        
        return base_gas
    
    def _estimate_deployment_cost(self, project: CryptoProject) -> float:
        """Estimate deployment cost in ETH"""
        gas = self._estimate_gas(project)
        gas_price_gwei = 50  # Assume 50 gwei
        
        cost_eth = (gas * gas_price_gwei) / 1e9
        return cost_eth
    
    def _generate_contract_address(self) -> str:
        """Generate a contract address"""
        import secrets
        return '0x' + secrets.token_hex(20)
    
    def _generate_tx_hash(self) -> str:
        """Generate a transaction hash"""
        import secrets
        return '0x' + secrets.token_hex(32)
    
    def _get_explorer_url(self, network: str, address: str) -> str:
        """Get block explorer URL"""
        explorer_map = {
            'ethereum_mainnet': f'https://etherscan.io/address/{address}',
            'ethereum_goerli': f'https://goerli.etherscan.io/address/{address}',
            'binance_mainnet': f'https://bscscan.com/address/{address}',
            'binance_testnet': f'https://testnet.bscscan.com/address/{address}',
        }
        return explorer_map.get(network, '')
    
    def _save_project(self, project: CryptoProject):
        """Save project to disk"""
        filepath = self.projects_dir / f"{project.project_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(project.to_dict(), f, indent=2)
    
    def _load_projects(self):
        """Load all projects from disk"""
        for filepath in self.projects_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                project_id = data['project_id']
                logger.info(f"Loaded project: {data['name']} ({project_id})")
                
            except Exception as e:
                logger.error(f"Error loading project from {filepath}: {e}")
