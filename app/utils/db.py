import logging
from sqlalchemy import create_engine
from app.config import Config
from sqlalchemy.pool import QueuePool
from app.models import Base


logger = logging.getLogger(__name__)


def get_database_url():
    return (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}"
        f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}?charset={Config.DB_CHARSET}"
    )


# 创建数据库的连接引擎
engine = create_engine(
    get_database_url(),  # 数据库的连接地址URL
    poolclass=QueuePool,  # 数据库连接池
    pool_size=10,  # 数据库连接池中的最大连接数
    max_overflow=20,  # 允许 最大溢出连接 数量为20
    pool_pre_ping=True,  # 连接每次获取 前先检查可用性
    pool_recycle=3600,  # 3600秒如果不使用回收连接
    echo=False,  # 不输出SQL日志
)


def init_db():
    try:
        # 使用引擎来创建数据库的表结构
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.error(f"初始化数据库失败:{e}")
        raise
