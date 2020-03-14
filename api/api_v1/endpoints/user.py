from datetime import timedelta

from fastapi import Security, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from db.userModel import User
from validator.schemas import Token, UserValidator
from utils.jwt_service import get_current_user, create_access_token, get_password_hash, verify_password

#######################################################################################
# Param Data @
# Return @
# TODO @ 获取当前用户,需要身份验证
# *
# !
# ?
#######################################################################################


router = APIRouter()


@router.post("/token", response_model=Token)
# 第三方登录
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.objects.get(username=form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="该用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password):
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="密码错误", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=UserValidator, response_model_exclude=["password"])
# Security可以允许传入scopes的权限范围和Depends一样可以实现依赖注入
async def user(current_user: User = Security(get_current_user, scopes=["normal"])):
    return current_user
