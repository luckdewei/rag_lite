"""
蓝图模块
"""

from app.blueprints import auth, knowledgebase, settings
from flask import Blueprint, Flask
import pkgutil
import importlib


def register_blueprints(app: Flask):
    app.register_blueprint(auth.bp)
    app.register_blueprint(knowledgebase.bp)
    app.register_blueprint(settings.bp)


# __all__ = ["auth", "knowledgebase", "settings"]
