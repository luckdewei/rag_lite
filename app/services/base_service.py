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
