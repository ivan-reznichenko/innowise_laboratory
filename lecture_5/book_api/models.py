# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Book(Base):
    """
    SQLAlchemy model representing the 'books' table in the database.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=True)