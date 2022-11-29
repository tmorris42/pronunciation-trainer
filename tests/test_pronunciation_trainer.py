"""Tests for pronunciation_trainer.py"""

import unittest
from unittest.mock import Mock

import pronunciation_trainer.pronunciation_trainer as pt
from pronunciation_trainer.pronunciation_trainer import App


class TestApp(unittest.TestCase):
    """Tests for the App class"""

    def test_ulog(self):
        """Tests for ulog"""
        pt.tk = Mock()
        app = App(Mock())
        app.window.log = Mock()
        app.window.log.set = Mock()
        app.ulog("HelloWorld!")
        app.window.log.set.assert_called_once_with("HelloWorld!")
