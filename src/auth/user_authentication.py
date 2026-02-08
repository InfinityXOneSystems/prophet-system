"""
User Authentication System
==========================

Secure user authentication and management for the leaderboard system.
"""

import hashlib
import json
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger('X1_PREDICT.AUTH')


@dataclass
class User:
    """User account representation"""
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    display_name: str = ""
    avatar_url: str = ""
    bio: str = ""
    total_portfolios: int = 0
    total_trades: int = 0
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email if include_sensitive else '',
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'display_name': self.display_name or self.username,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'total_portfolios': self.total_portfolios,
            'total_trades': self.total_trades,
            'member_since_days': (datetime.now() - self.created_at).days
        }
        if include_sensitive:
            data['password_hash'] = self.password_hash
        return data


@dataclass
class Session:
    """User session"""
    session_id: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    user_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=7))
    is_active: bool = True
    last_activity: datetime = field(default_factory=datetime.now)
    
    def is_valid(self) -> bool:
        return self.is_active and datetime.now() < self.expires_at
    
    def refresh(self):
        self.last_activity = datetime.now()
        self.expires_at = datetime.now() + timedelta(days=7)


class UserAuthenticationSystem:
    """User Authentication System"""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.users_dir = self.data_dir / 'users'
        self.sessions_dir = self.data_dir / 'sessions'
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.username_to_id: Dict[str, str] = {}
        self._load_users()
        logger.info(f"UserAuthenticationSystem initialized")
    
    def register_user(self, username: str, password: str, email: str, display_name: str = "") -> Optional[User]:
        if not username or len(username) < 3:
            logger.error("Username must be at least 3 characters")
            return None
        if username.lower() in [u.lower() for u in self.username_to_id.keys()]:
            logger.error(f"Username '{username}' already exists")
            return None
        if not password or len(password) < 6:
            logger.error("Password must be at least 6 characters")
            return None
        user = User(username=username, email=email, password_hash=self._hash_password(password), display_name=display_name or username)
        self.users[user.user_id] = user
        self.username_to_id[username.lower()] = user.user_id
        self._save_user(user)
        logger.info(f"Registered new user: {username}")
        return user
    
    def login(self, username: str, password: str) -> Optional[Session]:
        user_id = self.username_to_id.get(username.lower())
        if not user_id:
            return None
        user = self.users.get(user_id)
        if not user or not user.is_active:
            return None
        if not self._verify_password(password, user.password_hash):
            return None
        session = Session(user_id=user.user_id)
        self.sessions[session.session_id] = session
        self._save_session(session)
        user.last_login = datetime.now()
        self._save_user(user)
        logger.info(f"User '{username}' logged in")
        return session
    
    def verify_session(self, session_id: str) -> Optional[User]:
        session = self.sessions.get(session_id)
        if not session or not session.is_valid():
            return None
        session.refresh()
        return self.users.get(session.user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        user_id = self.username_to_id.get(username.lower())
        return self.users.get(user_id) if user_id else None
    
    def update_user_stats(self, user_id: str, total_portfolios: int = None, total_trades: int = None) -> bool:
        user = self.users.get(user_id)
        if not user:
            return False
        if total_portfolios is not None:
            user.total_portfolios = total_portfolios
        if total_trades is not None:
            user.total_trades = total_trades
        self._save_user(user)
        return True
    
    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        try:
            salt, pwd_hash = password_hash.split('$')
            check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return check_hash == pwd_hash
        except Exception:
            return False
    
    def _save_user(self, user: User):
        filepath = self.users_dir / f"{user.user_id}.json"
        with open(filepath, 'w') as f:
            json.dump(user.to_dict(include_sensitive=True), f, indent=2)
    
    def _save_session(self, session: Session):
        filepath = self.sessions_dir / f"{session.session_id}.json"
        data = {'session_id': session.session_id, 'user_id': session.user_id, 'created_at': session.created_at.isoformat(), 'expires_at': session.expires_at.isoformat(), 'is_active': session.is_active}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_users(self):
        for filepath in self.users_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.username_to_id[data['username'].lower()] = data['user_id']
            except Exception as e:
                logger.error(f"Error loading user: {e}")
