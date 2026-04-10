from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FriendRequestCreate(BaseModel):
    # The user ID to send a friend request to
    addressee_id: str


class FriendshipStatusUpdate(BaseModel):
    # Accepted values: "accepted" or "declined"
    status: str


class FriendOut(BaseModel):
    # Represents a confirmed friend in the friend list
    id: str
    username: str
    model_config = ConfigDict(from_attributes=True)


class FriendRequestOut(BaseModel):
    # Represents a pending friend request
    id: int
    requester_id: str
    addressee_id: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
