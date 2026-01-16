from flask import Flask
import os
from app.config import Config
from flask_cors import CORS
from app.utils.auth import get_current_user
from app.utils.logger import get_logger

# 导入初始化数据库的函数
from app.utils.db import init_db


def create_app(config_class=Config):

    # 获取名为当前的模块名的日志记录器
    logger = get_logger(__name__)
    try:
        logger.info("初始化数据库...")
        init_db()
        logger.info("初始化数据库成功")
    except Exception as e:
        logger.warning(f"数据库初始化失败{e}")

    # 获取当前文件所在的目录的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )

    # 注册上下文管理器，使current_user指向当前登录的用户，并且在所有的模板里可用
    @app.context_processor
    def inject_user():
        return dict(current_user=get_current_user())

    from app.blueprints import auth, knowledgebase

    app.register_blueprint(auth.bp)
    app.register_blueprint(knowledgebase.bp)

    app.config.from_object(config_class)

    # 启用请求支持
    CORS(app)

    return app
