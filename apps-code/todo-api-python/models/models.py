from sqlalchemy import Column, Integer, String

from database.database import Base


class TodoItem(Base):
    """SQLAlchemy model for a todo item."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
