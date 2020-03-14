# 基于 FastAPI 项目记录

---

### 第一个 FastAPI 程序

- 创建虚拟环境

```
python3 -m venv .fastapi
```

- 激活虚拟环境

```
source .fastapi/bin/activate
```

- 安装基础依赖

```
pip install fastapi unicorn
```

- 最简单的例子

```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

- 启动项目

```
uvicorn main:app --reload
```

- 接口文档
```
/redoc /docs
```
- 安装依赖
``` 
pip install -r requirements.txt
```
- 导出依赖 
```
pip freeze > requirements.txt
```
---

### 项目解耦

- 思路: main.py 中的流程

1. 初始化配置(mysql, redis, mongodb 等)
   > 单独拎出来一个文件再分别引 redis/init.py db/init.py 等初始化连接配置.可以参考 Gin 的拆分方式(注意要打好日志, 用 try finally 起服务)
2. add_router()添加路由, 在 api/api_v1/api.py 做分组, 然后引 endpionts 中的子路由模块
3. 最后 run 起项目来 if **name**==**main**

- 解耦出来的包功能说明

1. utils: 工具包
2. alambic: 数据库迁移工具自动创建的包
3. api: 项目路由, api_v1:第一版, api.py:分组路由, endpoint:真正的子路由
4. crud: 各种资源的增删改查数据库操作, 与 service(endpoints)要解耦
5. db: 数据库的连接
6. model: ORM(sqlalchemy)
7. validator: pydantic 库的校验
8. settings: 项目的配置文件, 不能暴露给用户
9. common: 公共依赖
10. service : 业务逻辑
11. test : 测试

---

### 数据库迁移

- 配合 sqlalchemy 的数据库迁移工具

```
pip install alembic
```

- 项目初始化文件夹, 用来配置迁移文件和存放迁移历史记录

```
alembic init alembic
```

- 配置你的数据库连接

```
sqlalchemy.url = driver://user:pass@localhost/dbname
```

- 修改 env.py 文件

```
target_metadata = None
```

```
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))
# 注意这个地方是要引入模型里面的Base,不是connect里面的
from sqlalchemy_demo.modules.user_module import Base
target_metadata = Base.metadata
```

- 创建迁移文件

```
alembic revision --autogenerate -m "描述信息类似于git"
```

- 更新到最新的版本

```
alembic upgrade head
```

- 更多功能请查看官网

---

### 项目的设计细节

- 可以参考官方文档的 sqlachemy 例子
