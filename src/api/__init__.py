"""
AI Prophet - API Module
Contains API and dashboard components.
"""

from .dashboard_api import create_app, run_server

__all__ = [
    'create_app',
    'run_server',
]
