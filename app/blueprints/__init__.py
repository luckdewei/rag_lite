"""
蓝图模块
"""

from app.blueprints import auth, knowledgebase, settings, document
from flask import Flask


def register_blueprints(app: Flask):
    app.register_blueprint(auth.bp)
    app.register_blueprint(knowledgebase.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(document.bp)


# __all__ = ["auth", "knowledgebase", "settings"]
