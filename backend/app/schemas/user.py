from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: str
    username: str
    # Allows Pydantic to read SQLAlchemy ORM objects directly
    model_config = ConfigDict(from_attributes=True)
