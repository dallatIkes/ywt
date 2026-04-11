from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FriendRequestCreate(BaseModel):
    addressee_id: str


class FriendshipStatusUpdate(BaseModel):
    status: str


class FriendOut(BaseModel):
    id: str
    username: str
    model_config = ConfigDict(from_attributes=True)


class FriendRequestOut(BaseModel):
    # Enriched — used for pending lists (includes usernames)
    id: int
    requester_id: str
    requester_username: str
    addressee_id: str
    addressee_username: str
    status: str
    created_at: datetime


class FriendshipOut(BaseModel):
    # Simple — used for send/respond (ORM object, no join needed)
    id: int
    requester_id: str
    addressee_id: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
