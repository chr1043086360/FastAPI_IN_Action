#######################################################################################
# Param Data @
# Return @
# TODO @ 项目入口文件
# *
# !
# ?
#######################################################################################

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api_v1.api import api_router
from db.init_db import create_connection, disconnect

#  可以像flask一样自定义一些配置
app = FastAPI(openapi_url="/api/v1/openapi.json")

# 初始化数据库连接
# init_db()

app.add_event_handler("startup", create_connection)
app.add_event_handler("shutdown", disconnect)

# CORS配置
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# *添加路由规则
app.include_router(api_router, prefix="/api/v1")  # 默认的前缀


@app.get("/")
async def index():
    return {"ping": "pong"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
