from app.infrastructure.database.base import Base

from sqlalchemy import Column, UUID, String, Integer
import uuid


class UserModel(Base):
    __tablename__ = "user_workers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    avatar_url = Column(String, default=None)
    age = Column(Integer, default=None)
    resume = Column(String, default=None)