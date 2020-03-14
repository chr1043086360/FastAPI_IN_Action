#######################################################################################
# Param Data @
# Return @
# TODO @ OAuth2.0 + JWT 登录接口，Bearer token，一般放在请求头中Authorization
# * 例：“eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Imxpbmlhbmh1aSJ9.hnOfZb95jFwQsYj3qlgFbUu1rKpfTE6AzgXZidEGGTk”
# * 由header.payload.signature三部分组成,通过Base64编码
# * header：{"alg": "HS256","typ": "JWT"}token类型和签名算法
# * payload:{"sub":xxxxxx, "name":xxxxxx}jwt中预定的了一些claims
# * signature:对前两部分的摘要进行签名
# !
# ?
#######################################################################################
"""
JWT中预制了一些Claim :
1.iss（Issuer签发者）
2.sub（subject签发给的受众，在Issuer范围内是唯一的）
3.aud（Audience接收方）
4.exp（Expiration Time过期时间）
5.iat（Issued At签发时间）等等

如果放在cookie中觉得浪费带宽可以放在请求头中

OAuth2.0和JWT结合使用 :
{
    "sub":"xxxxxx",
    "scope":"normal",
    "exp":xxx,
}
"""

from fastapi import Body, APIRouter, HTTPException, status, Response
from validator.schemas import Token
from db.userModel import User
from utils.jwt_service import create_access_token,  verify_password


router = APIRouter()


# 登录接口
@router.post("/login", response_model=Token)
async def login(response: Response, username: str = Body(..., min_length=6), password: str = Body(..., min_length=6)):
    # 获取用户
    user = await User.objects.get(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用不存在",
            headers={"Authorization": "Bearer"},
        )

    # 验证密码
    if not verify_password(password, user.password):
        return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="密码错误")

    # 根据username生成JWT token
    token = create_access_token(
        data={"sub": user.username, "scopes": [user.permission]})

    if token:
        # 这里可以不在后端set_cookie，vue也可以做，比较通用的是在前端做，因为安卓和ios是不支持cookie的
        # cookie的过期时间要和jwt token过期时间保持一致
        response.set_cookie("JWT-token", token, expires=15*60,
                            path="/", domain="127.0.0.1", httponly=True)

        return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="生成token失败")
