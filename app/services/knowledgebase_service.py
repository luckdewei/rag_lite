from app.models.knowledgebase import Knowledgebase
from app.services.base_service import BaseService
import os
from app.services.storage_service import storage_service
from app.config import Config
from sqlalchemy.exc import IntegrityError


class KnowledgebaseService(BaseService[Knowledgebase]):
    def create(
        self,
        name,
        user_id,
        description,
        chunk_size,
        chunk_overlap,
        cover_image_data,
        cover_image_filename,
    ):
        if cover_image_data and cover_image_filename:
            # 获取不带.的文件扩展名
            file_ext_without_dot = (
                os.path.splitext(cover_image_filename)[1][1:].lower()
                if "." in cover_image_filename
                else ""
            )
            if not file_ext_without_dot:
                raise ValueError(f"文件缺少扩展名:{cover_image_filename}")
            if file_ext_without_dot not in Config.ALLOWED_IMAGE_EXTENSIONS:
                raise ValueError(
                    f"不支持的图片格式:{file_ext_without_dot},支持的格式为{', '.join(Config.ALLOWED_IMAGE_EXTENSIONS)}"
                )
            if len(cover_image_data) == 0:
                raise ValueError(f"上传的图片为空")
            if len(cover_image_data) > Config.MAX_IMAGE_SIZE:
                raise ValueError(
                    f"图片大小已经超过了最大限制:{Config.MAX_IMAGE_SIZE/1024/1024}M"
                )

        try:
            with self.transaction() as session:
                kb = Knowledgebase(
                    name=name,
                    user_id=user_id,
                    description=description,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
                # 将知识库对象添加到session
                session.add(kb)
                # 刷新session,生成知识库的ID
                session.flush()
                if cover_image_data and cover_image_filename:
                    # 构建封面图片的路径  统一使用小写扩展名 .png .jpg .gif 带点的文件扩展名
                    file_ext_with_dot = os.path.splitext(cover_image_filename)[
                        1
                    ].lower()
                    cover_image_path = f"covers/{kb.id}{file_ext_with_dot}"
                    self.logger.info(
                        f"正在为新的知识库{kb.id}上传封面图片，文件名:{cover_image_filename},路径:{cover_image_path}"
                    )
                    storage_service.upload_file(cover_image_path, cover_image_data)
                    self.logger.info(f"成功上传知识库的封面图片:{cover_image_path}")
                    kb.cover_image = cover_image_path
                    session.flush()
                # 刷新kb对象的数据库状态
                session.refresh(kb)
                # 把模型实例转成字典
                kb_dict = kb.to_dict()
                self.logger.info("创建知识库成功:ID:{kb.id}")
                return kb_dict
        except IntegrityError:
            raise ValueError("该用户下已存在同名知识库")

    def list(self, user_id, page, page_size, search, sort_by, sort_order):
        with self.session() as session:
            query = session.query(Knowledgebase)
            # 如果指定了user_id，则只查找该 用户的知识库
            if user_id:
                query = query.filter(Knowledgebase.user_id == user_id)
            if search:
                search_pattern = f"%{search}%"
                query = query.filter(
                    (Knowledgebase.name.like(search_pattern))
                    | (Knowledgebase.description.like(search_pattern))
                )
            sort_field = None
            if sort_by == "name":
                sort_field = Knowledgebase.name
            elif sort_by == "updated_at":
                sort_field = Knowledgebase.updated_at
            else:
                sort_field = Knowledgebase.created_at
            if sort_order == "asc":
                query = query.order_by(sort_field.asc())
            else:
                query = query.order_by(sort_field.desc())
            # 统计总记录数
            total = query.count()
            # 计算分页的偏移量
            offset = (page - 1) * page_size
            kbs = query.offset(offset).limit(page_size).all()
            items = []
            for kb in kbs:
                items.append(kb.to_dict())
            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
            }

    def delete(self, kb_id):
        with self.transaction() as session:
            kb = session.query(Knowledgebase).filter(Knowledgebase.id == kb_id).first()
            if not kb:
                return False
            session.delete(kb)
            self.logger.info(f"删除知识库:{kb_id} {kb.name}")
            return True

    #   def get_by_id(self, kb_id):
    #       kb = super().get_by_id(Knowledgebase, kb_id)
    #       if kb:
    #           return kb.to_dict()
    #       return None
    def get_by_id(self, kb_id: str):
        with self.session() as db_session:
            try:
                return (
                    db_session.query(Knowledgebase)
                    .filter(Knowledgebase.id == kb_id)
                    .first()
                    .to_dict()
                )
            except Exception as e:
                self.logger.error("获取ID对应的对象失败:{e}")
                return None

    def update(
        self, kb_id, cover_image_data, cover_image_filename, delete_cover, **kwargs
    ):
        with self.transaction() as session:
            kb = session.query(Knowledgebase).filter(Knowledgebase.id == kb_id).first()
            if not kb:
                return None
            # 老的图片路径
            old_cover_path = kb.cover_image if kb.cover_image else None
            if delete_cover:
                if old_cover_path:
                    # 如果有旧的封面图片，并且需要删除的话
                    storage_service.delete_file(old_cover_path)
                    self.logger.info(f"已成功删除旧的封面图片:{old_cover_path}")
                    # 更新数据库中的cover_image为None
                    setattr(kb, "cover_image", None)
            elif cover_image_data and cover_image_filename:
                file_ext_with_dot = os.path.splitext(cover_image_filename)[1]
                file_ext_with_dot = file_ext_with_dot.lower()
                # 构建新的图片路径
                new_cover_path = f"covers/{kb_id}{file_ext_with_dot}"
                if old_cover_path:
                    storage_service.delete_file(old_cover_path)
                storage_service.upload_file(new_cover_path, cover_image_data)
                setattr(kb, "cover_image", new_cover_path)

            for key, value in kwargs.items():
                if hasattr(kb, key) and value is not None:
                    setattr(kb, key, value)
            # flush指是使用我们提供的kb的值去更新数据库
            session.flush()
            # 刷新对象，避免未提交前读到旧的数据
            session.refresh(kb)
            kb_dict = kb.to_dict()
            self.logger.info(f"更新知识库:{kb_id} {kb.name}")
            return kb_dict


kb_service = KnowledgebaseService()
