from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# ORM models

class Post(Base):
    __tablename__ = "posts"

    idPost = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    created_at =Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    idUser = Column(Integer,ForeignKey("users.idUser",ondelete="CASCADE"),nullable=False)

    owner = relationship("User") # Relationship between class Post and class User

class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)
    idUser = Column(Integer, primary_key=True, nullable=False)
    created_at =Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    idUser = Column(Integer, ForeignKey("users.idUser" , ondelete="CASCADE"),nullable=False , primary_key=True)
    idPost = Column(Integer,ForeignKey("posts.idPost", ondelete="CASCADE"),nullable=False, primary_key=True)
    


