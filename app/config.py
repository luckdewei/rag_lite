import os
from pathlib import Path


class Config:
    #  项目根目录的路径
    BASE_DIR = Path(__file__).parent.parent
    # 加载环境变量中配置的密钥
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # 应用配置
    # 应用监听的主机地址
    APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
    # 服务器监听的端口号
    APP_PORT = os.environ.get("APP_PORT", 5000)
    # 是否启动调用模式
    APP_DEBUG = os.environ.get("APP_DEBUG", "false").lower() == "true"
    # 上传的文件的最大文件大小
    MAX_FILE_SIZE = os.environ.get("MAX_FILE_SIZE", 104857600)  # 100M
    # 允许 上传的文件
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "md"}

    # 日志配置
    # 日志存放目录
    LOG_DIR = os.environ.get("LOG_DIR", "./logs")
    # 日志文件
    LOG_FILE = os.environ.get("LOG_FILE", "rag_lite.log")
    # 日志级别
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    # 是否启用文件日志
    LOG_ENABLE_FILE = os.environ.get("LOG_ENABLE_FILE", "true").lower() == "true"
    # 是否启用控制台
    LOG_ENABLE_CONSOLE = os.environ.get("LOG_ENABLE_CONSOLE", "true").lower() == "true"
