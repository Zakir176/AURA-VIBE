from pydantic import BaseModel
from typing import List, Optional

class QueueItem(BaseModel):
    session_code: str
    song_title: str
    song_url: str
    added_by: str

    class Config:
        from_attributes = True

class QueueReorder(BaseModel):
    session_code: str
    order: List[int]  # Array of queue IDs in new order

class QueueItemResponse(QueueItem):
    id: int
    votes: int
    played: bool
    position: int

    class Config:
        from_attributes = True