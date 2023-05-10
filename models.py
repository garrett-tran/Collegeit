"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# TODO: Complete your models

class User(Base):
    __tablename__ = "users"

    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    def __repr__(self):
        return "@" + self.username
    
class College(Base):
    __tablename__ = "colleges"

    name = Column("name", TEXT, primary_key=True)
    class_size = Column("class_size", INTEGER, nullable=False)
    average_sat = Column("average_sat", INTEGER, nullable=False)

    def __repr__(self):
        return "@" + self.username
    

class CollegesFollowed(Base):
    __tablename__ = "collegesfollowed"
    id = Column("id", INTEGER, primary_key=True)
    user_username = Column("user_username", TEXT, ForeignKey('users.username'))
    college_name = Column("college_name", TEXT, ForeignKey('colleges.name'))

class Post(Base):
    __tablename__ = "posts"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT, nullable = False)
    post_username = Column("username", TEXT, ForeignKey("users.username"))
    post_college = Column("college", TEXT, ForeignKey("colleges.name"))
    timestamp = Column("timestamp", TEXT, nullable = False)
    tags = relationship("Tag", secondary = "posttags", back_populates = "posts")
    def __repr__(self):
        tags = ""
        for tag in self.tags:
            tags += "#" + str(tag) + " "
        return tags

class Tag(Base):
    __tablename__ = "tags"
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT, nullable = False)
    posts = relationship("Post", secondary = "posttags", back_populates = "tags")
    def __repr__(self):
        return self.content

class PostTag(Base):
    __tablename__ = "posttags"
    id = Column("id", INTEGER, primary_key=True)
    tag_id = Column("tag_id", INTEGER, ForeignKey('tags.id'))
    post_id = Column("post_id", INTEGER, ForeignKey('posts.id'))