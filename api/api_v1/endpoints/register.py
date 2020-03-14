#######################################################################################
# Param Data @
# Return @
# TODO @ 注册接口
# *
# !
# ?
#######################################################################################

from fastapi import APIRouter, HTTPException, status
from validator import schemas
from common.BaseResponse import BaseResponse
from db.userModel import User
from utils.jwt_service import create_access_token, get_password_hash
from pymysql.err import IntegrityError


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user_schema: schemas.UserValidator):

    # 可以在schema里校验，但是比较费劲就在这里校验了
    if len(user_schema.username) <= 6 or len(user_schema.password) <= 6:
        raise HTTPException(422, detail="用户名和密码不能小于6位")

    # 对密码加密
    hash_password = get_password_hash(user_schema.password)
    try:
        # 在数据库中创建记录
        await User.objects.create(username=user_schema.username, password=hash_password)

    except IntegrityError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="该用户名已经有人创建")

    # 发放token
    token = create_access_token(data={"username": user_schema.username})
    data = {
        "token": token,
        "token_type": "bearer"
    }

    return BaseResponse(code=201, msg="用户创建成功", data=data)
