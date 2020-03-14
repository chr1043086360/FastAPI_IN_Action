import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
# 注意fastapi包中的HTTPException才可以定义请求头
from fastapi import Depends, status, HTTPException
# from starlette.exceptions import HTTPException
from pydantic import ValidationError
from validator.schemas import TokenData
from db.userModel import User

#######################################################################################
# Param Data @
# Return @
# TODO @ jwt工具包
# *
# !
# ?
#######################################################################################

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=['bcrypt'])

# 这里的tokenUrl路径一定要和token路径保持一致
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token", scopes={
                                     "normal": "Read information about current user", "admin": "admin user"})


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# hash密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 创建jwt-token
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 获取当前用户
async def get_current_user(*, token: str = Depends(oauth2_scheme), security_scopes: SecurityScopes):
    if security_scopes.scopes:
        # 固定的写法，见官网
        authenticate_value = f"Bearer scopes={security_scopes.scope_str}"

    else:
        authenticate_value = f"Bearer"

    # 这里定义一个通用的错误
    error = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="无权访问",
                          headers={"WWW-Authenticate": authenticate_value})

    try:
        # 解码token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 按照OAuth2.0通常定义成“sub”
        username = payload.get("sub")

        if username is None:
            raise error
        # scopes是权限，在上面已经定义
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)

    except (PyJWTError, ValidationError):
        raise error

    #　解码成功获取到user
    user = await User.objects.limit(1).filter(username=username).all()

    if user is None:
        raise error

    # 判断权限
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    # 返回用户
    return user[0]
