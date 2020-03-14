# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean, Text
# from sqlalchemy.orm import relationship
# from db.init_db import init_db

# Base = declarative_base()

# _, engine = init_db()
# Base.metadata.create_all(bind=engine)


#######################################################################################
# Param Data @
# Return @
# TODO @ 基本的sqlalchemy orm
# *
# !
# ?
#######################################################################################

# class User(Base):

#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(32))
#     username = Column(String(32), nullable=False, unique=True)
#     password = Column(String(60), nullable=False)
#     nickname = Column(String(32))
#     phoneNum = Column(Integer)
#     email = Column(String(30))
#     create_time = Column(Time)
#     delete_time = Column(Time)
#     birth_year = Column(Integer, default=2000)
#     birth_month = Column(Integer, default=1)
#     birth_day = Column(Integer, default=1)
#     avatar = Column(String(256))
#     sex = Column(Boolean)
#     location = Column(String(32))
#     # 用户类型
#     # CHOICES
#     # type
#     token = Column(String(60), default="666")
#     todo_list = relationship('todoList', back_populates="users")


# class todoList(Base):

#     __tablename__ = "todoList"

#     id = Column(String(20), primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     users = relationship('User', back_populates="todo_list")
#     title = Column(String(30), nullable=False)
#     status = Column(Boolean, default=0)
#     info = Column(Text)
#     created_at = Column(Time)
#     updated_at = Column(Time)
#     deleted_at = Column(Time)

#######################################################################################
# Param Data @
# Return @
# TODO @ orm为基于sqlalchemy的异步数据库迁移模型，依赖aiomysql
# *
# !
# ?
#######################################################################################
import orm

from db.init_db import database, metadata


class User(orm.Model):

    __tablename__ = "user"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    username = orm.String(max_length=50,  allow_null=False,
                          allow_blank=False, index=True, unique=True)
    email = orm.String(max_length=50, unique=True, index=True, allow_null=True,
                       allow_blank=True)
    password = orm.String(max_length=255, allow_null=False,
                          allow_blank=False)
    phone = orm.String(max_length=11, min_length=11,
                       allow_null=True, allow_blank=True)
    # 用户权限scopes字段
    permission = orm.String(max_length=50, default="normal",
                            allow_null=True, allow_blank=True)
    created_at = orm.String(allow_null=True, allow_blank=True, max_length=50)
    updated_at = orm.String(allow_null=True, allow_blank=True, max_length=50)
    deleted_at = orm.String(allow_null=True, allow_blank=True, max_length=50)
    # 外键
    # todo = orm.ForeignKey(TodoList)
