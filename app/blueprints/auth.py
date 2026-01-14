# 认证相关路由（视图）
"""
认证相关路由（视图）
"""
# 导入 Flask 所需模块和方法
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 导入日志模块
from app.utils.logger import get_logger

logger = get_logger(__name__)

bp = Blueprint("auth", __name__)


@bp.route("/")
def home():
    return render_template("home.html")
