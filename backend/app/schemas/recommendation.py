from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class RecoCreate(BaseModel):
    link: str
    description: str = Field(max_length=280)
    to_user_id: str


class RatingUpdate(BaseModel):
    # Only field the recipient can update on a received recommendation
    rating: int = Field(ge=1, le=5)


class RecoOut(BaseModel):
    id: int
    link: str
    description: str
    from_user_id: str
    to_user_id: str
    rating: int | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RecoSentOut(BaseModel):
    # Outbound view — shows recipient username instead of raw ID
    id: int
    link: str
    description: str
    to_user: str
    rating: int | None
    created_at: datetime


class RecoReceivedOut(BaseModel):
    # Inbound view — shows sender username instead of raw ID
    id: int
    link: str
    description: str
    from_user: str
    rating: int | None
    created_at: datetime
