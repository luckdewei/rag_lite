# 用户模型说明文档字符串
"""
用户模型
"""

# 从 SQLAlchemy 导入 Column、String、DateTime、Boolean 类型
from sqlalchemy import Column, String, DateTime, Boolean

# 从 SQLAlchemy 导入 func 用于处理时间戳
from sqlalchemy.sql import func

# 导入 uuid 模块用于生成唯一标识符
import uuid

# 从项目模型基类导入 BaseModel
from app.models.base import BaseModel


# 声明 User 用户模型，继承自 BaseModel
class User(BaseModel):
    # 用户模型的类说明
    """用户模型"""
    # 指定数据表名称为 'user'
    __tablename__ = "user"
    # 指定 __repr__ 时显示的字段为 id 和 username
    __repr_fields__ = ["id", "username"]  # 指定 __repr__ 显示的字段

    # 用户主键 id，使用 uuid 生成，字符串32位
    id = Column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:32])
    # 用户名字段，必填，唯一且建立索引，最大长度64
    username = Column(String(64), nullable=False, unique=True, index=True)
    # 邮箱字段，可以为空，唯一且建立索引，最大长度128
    email = Column(String(128), nullable=True, unique=True, index=True)
    # 密码哈希字段，必填，最大长度255
    password_hash = Column(String(255), nullable=False)  # 存储密码哈希
    # 用户是否激活，默认为激活（True），不可为空
    is_active = Column(Boolean, nullable=False, default=True)
    # 创建时间字段，默认当前时间，建立索引
    created_at = Column(DateTime, default=func.now(), index=True)
    # 更新时间字段，默认当前时间，更新时自动刷新
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 将当前用户对象转换为字典
    def to_dict(self, include_password=False, **kwargs):
        # 转换为字典，如果未包含密码，排除 password_hash 字段
        """转换为字典"""
        exclude = ["password_hash"] if not include_password else []
        # 调用父类的 to_dict 方法，传入要排除的字段
        return super().to_dict(exclude=exclude, **kwargs)
