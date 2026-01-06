from pydantic import BaseModel, Field

class UserBody(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    
class RecoBody(BaseModel):
    link: str
    from_user_id: int
    to_user_id: int
    
class Token(BaseModel):
    access_token: str
    token_type: str