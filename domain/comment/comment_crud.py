from sqlalchemy.orm import Session
from domain.comment.comment_schema import CommentCreate
from models import Comment
from datetime import datetime

def create_comment(db: Session, comment_create: CommentCreate, user_id: int):
    db_comment = Comment(
        content=comment_create.content,
        create_date=datetime.now(),
        user_id=user_id,
        question_id=comment_create.question_id,
        answer_id=comment_create.answer_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
