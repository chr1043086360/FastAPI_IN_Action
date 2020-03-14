from db.init_db import metadata

# 这里这儿写是为了统一暴露metadata，在数据库迁移时可以找到模型
from .todoModel import TodoList
from .userModel import User