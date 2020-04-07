# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
import databases
import sqlalchemy

#######################################################################################
# Param Data @
# Return @
# TODO @ 基本的sqlalchemy配置
# *
# !
# ?
#######################################################################################
# def init_db():
#     # echo=True: 输出sqlalchemy日志
#     engine = create_engine(
#         f"mysql+pymysql://root:{MYSQL_PASSWORD}@{HOST_IP}:3306/{MYSQL_NAME}", echo=False)
#     # 创建DBSession类型
#     SessionLocal = sessionmaker(bind=engine)
#     return SessionLocal, engine


# Dependency
# def get_db():
#     sessionLocal, _ = init_db()
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#######################################################################################
# Param Data @
# Return @
# TODO @ orm为基于sqlalchemy的异步数据库迁移模型，依赖aiomysql
# *
# !
# ?
#######################################################################################
from settings.config import DATABASE_PASSWORD, HOST_IP
DATABASE_URL = f"mysql+pymysql://root:{DATABASE_PASSWORD}@{HOST_IP}:3306/fastapi_plus"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)


async def create_connection():
    await database.connect()


async def disconnect():
    await database.disconnect()
