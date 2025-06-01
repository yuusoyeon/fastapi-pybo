from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from domain.comment import comment_crud, comment_schema
from database import get_db
from models import Comment
from models import User
from domain.user.user_router import get_current_user

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

@router.post("/create", response_model=comment_schema.Comment)
def create_comment(
    comment_create: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return comment_crud.create_comment(db, comment_create, current_user.id)