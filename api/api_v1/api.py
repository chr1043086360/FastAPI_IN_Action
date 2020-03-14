from fastapi import APIRouter

from api.api_v1.endpoints import user, login, register

api_router = APIRouter()

# 分组路由
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
# api_router.include_router(utils.router, prefix="/util", tags=["utils"])
api_router.include_router(register.router, tags=["register"])
