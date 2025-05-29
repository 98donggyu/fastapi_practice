from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

# FastAPI() 객체 생성
app = FastAPI()

abs_path = os.path.dirname(os.path.realpath(__file__))

# html 템플릿을 사용하기 위한 설정
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더와 연동하기 위한 설정
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")


@app.get("/")
async def home(request: Request):
    todos = 0
    # html 파일에 데디터 렌더링해서 리턴한다는 의미
    return templates.TemplateResponse("index.html",
                                        {"request": request,
                                        "todos": todos})