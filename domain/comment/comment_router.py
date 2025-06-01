from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.comment import comment_crud, comment_schema
from database import get_db
from models import Comment

router = APIRouter(
    prefix="/api/comment",
    tags=["댓글"]
)

# ✅ 질문에 달린 댓글 조회
@router.get("/question/{question_id}", response_model=list[comment_schema.Comment])
def get_comments_by_question(question_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.question_id == question_id).order_by(Comment.create_date.asc()).all()

# ✅ 답변에 달린 댓글 조회
@router.get("/answer/{answer_id}", response_model=list[comment_schema.Comment])
def get_comments_by_answer(answer_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.answer_id == answer_id).order_by(Comment.create_date.asc()).all()
