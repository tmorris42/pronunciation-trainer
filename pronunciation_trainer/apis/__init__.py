"""Apis used in the pronunciation trainer"""
from .google import query_google_speech
from .sphinx import query_sphinx

__all__ = ["query_google_speech", "query_sphinx"]
