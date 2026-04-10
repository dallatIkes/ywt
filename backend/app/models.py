from pydantic import BaseModel, Field


class UserBody(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class RecoBody(BaseModel):
    link: str
    description: str = Field(max_length=280)
    to_user_id: str


class Token(BaseModel):
    access_token: str
    token_type: str
