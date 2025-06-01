from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ 라우터 import
from domain.question import question_router
from domain.user import user_router
from domain.answer import answer_router
from domain.comment import comment_router
app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # dev 환경 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(question_router.router)
app.include_router(comment_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
# ✅ 정적 파일은 dev 환경에선 굳이 필요 없음 (build된 파일 제공 X)
#    다만, 배포용 fallback이 필요하다면 유지 가능
