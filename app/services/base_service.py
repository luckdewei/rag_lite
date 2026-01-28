from app.utils.db import db_session, db_transaction
from typing import Optional, TypeVar, Generic, Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)
# 定义泛型的类型变量T
T = TypeVar("T")


# 定义基础服务器，支持泛型
class BaseService(Generic[T]):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def session(self):
        return db_session()

    def transaction(self):
        return db_transaction()

    def get_by_id(self, model_class: T, entity_id: str):
        with self.session() as db_session:
            try:
                return (
                    db_session.query(model_class)
                    .filter(model_class.id == entity_id)
                    .first()
                )
            except Exception as e:
                self.logger.error("获取ID对应的对象失败:{e}")
                return None

        # 定义通用的分页查询方法

    def paginate_query(
        self, query, page: int = 1, page_size: int = 10, order_by=None
    ) -> Dict[str, Any]:
        """
        通用分页查询方法
        Args:
            query: SQLAlchemy 查询对象（必须在 session 上下文中调用）
            page: 页码
            page_size: 每页数量
            order_by: 排序字段（可选，SQLAlchemy 表达式）
        Returns:
            包含 items, total, page, page_size 的字典
        """
        # 判断是否传入排序字段（注意不能直接 if order_by，否则部分 SQLAlchemy 表达式会抛异常）
        if order_by is not None:
            # 如传入排序条件则按该条件排序
            query = query.order_by(order_by)
        # 获取查询结果的总条数
        total = query.count()
        # 计算偏移量，例如第2页 offset=10 (从第11条开始)
        offset = (page - 1) * page_size
        # 查询当前页的数据
        items = query.offset(offset).limit(page_size).all()
        # 返回结果，items 为对象列表（支持自动 to_dict 转换），同时返回 total, page, page_size
        return {
            "items": [
                item.to_dict() if hasattr(item, "to_dict") else item for item in items
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
