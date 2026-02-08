"""
AI Prophet - Core Module
Contains core engine and learning components.
"""

from .prophet_core import AIProphet
from .recursive_learning import RecursiveLearningEngine

__all__ = [
    'AIProphet',
    'RecursiveLearningEngine',
]
