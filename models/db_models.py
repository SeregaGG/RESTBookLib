from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ARRAY
from db.database import Base


class Book(Base):
    __tablename__ = "books"

    # __table_args__ = (UniqueConstraint('author', 'title', name='uniq_book'),)

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String)
    genres = Column(ARRAY(String))
