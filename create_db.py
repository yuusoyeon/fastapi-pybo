# create_db.py
from database import Base, engine
from models import Question, Answer, User, Comment

# 테이블 생성
Base.metadata.create_all(bind=engine)
print("✅ 테이블 생성 완료!")