import os
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, SessionLocal 
from sqlalchemy.orm import Session
import models
from fastapi.responses import RedirectResponse

# models에 정의한 모델 클래스, 연결한 DB에 테이블을 생성함
models.Base.metadata.create_all(bind=engine)

# html 템플릿을 사용하기 위한 설정
abs_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=f"{abs_path}/templates")

app = FastAPI()

# static 폴더과 연동하기 위한 설정
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"))

# 의존성 주입을 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # todos 테이블 조회, 모든 todo 조회
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    # html 파일에 데이터 랜더링해서 리턴한다는 의미
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos" : todos}
    )
    
# 입력한 todo를 DB에 저장하기
@app.post("/add")
async def add(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    # DB 저장하기
    todo = models.Todo(task=task)
    db.add(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, "todo": todo, "todos" : todos}
        )

@app.post("/edit/{todo_id}")
async def add(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
