from typing import Union
from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: Union[str, None] = None
    exp: int = None



