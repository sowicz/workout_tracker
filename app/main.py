from fastapi import FastAPI, Request, Header, Form, Body
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
from pydantic import BaseModel
from typing import Union


app = FastAPI()
templates = Jinja2Templates(directory="./frontend/templates/")


app.mount("/static", StaticFiles(directory="static"), name="static")

data = []
ex = []

def cleardata():
    data.clear()
    ex.clear()


class Excercise(BaseModel):
    name: str
    quantity: Union[int, None] = None


@app.get("/index/", response_class=HTMLResponse)
async def index(request: Request):
    cleardata()
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.get("/app/", response_class=HTMLResponse)
async def appview(request: Request):
    cleardata()
    context = {"request": request}
    return templates.TemplateResponse("start_app.html", context)


@app.get("/tracking/", response_class=HTMLResponse)
async def tracking(request: Request):
    cleardata()
    context = {"request": request}
    return templates.TemplateResponse("tracking.html", context)


@app.get("/tracking-container/", response_class=HTMLResponse)
async def tracking(request: Request, bodypartSelect=Annotated[str, Body()]):    
    context = {"request": request, "bodypartSelect": bodypartSelect}
    parts = str(bodypartSelect)

    if data.count(parts)>0:
        print("Parts exist")
    elif bodypartSelect == "Choose...":
        print("bad choice")
    else:
        # bodypartSelect = {bodypartSelect}
        data.append(bodypartSelect)
        print(data)
        
        return templates.TemplateResponse("tracking-container.html", context)


# @app.get("/excercise/", response_class=HTMLResponse)
# async def excercise(request: Request):

#     context = {"request": request,}

#     return templates.TemplateResponse("excercise.html", context)


@app.post("/excercise/", response_class=HTMLResponse)
async def excercise(request: Request, excercise=Union[str, None]):

    excercise = "excercise"
    context = {"request": request, "excercise":excercise}
    ex.append(excercise)
    print(ex)
    print(len(ex))

    return templates.TemplateResponse("excercise.html", context)
