from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    content: str
    question_id: Optional[int] = None
    answer_id: Optional[int] = None

class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime
    question_id: Optional[int]
    answer_id: Optional[int]

    class Config:
        orm_mode = True
