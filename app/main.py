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

#clear workout data
def cleardata():
    data.clear()
    workout.workout_data.clear()


# Class workout to collect workout data
# function to add exercises 
# exercises with the same name won't be added to workout data
#

class Workout:
    def __init__(self):
        self.workout_data = {}
        self.series_num = 0

    def add_exercise(self, body_part, exercise_name):
        if body_part not in self.workout_data:
            self.workout_data[body_part] = []

        existing_part = self.workout_data.get(body_part)

        if existing_part is not None:
            existing_exercise = next((ex for ex in existing_part if ex["exerciseName"] == exercise_name), None)

        if existing_exercise is None:
            existing_part.append({"exerciseName": exercise_name, "sets": {}})






    def add_set(self, body_part, exercise_name, repetitions):
        existing_part = self.workout_data.get(body_part)
        if existing_part is not None:
            existing_exercise = next((ex for ex in existing_part if ex["exerciseName"] == exercise_name), None)
            if existing_exercise is not None:
                series_count = len(existing_exercise["sets"]) + 1
                self.series_num =series_count
                existing_exercise["sets"][series_count] = repetitions
        else:
            self.add_exercise(body_part, exercise_name)
            self.add_set(body_part, exercise_name, repetitions)


    def get_data(self):
        return self.workout_data



workout = Workout()



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



@app.get("/tracking-container/", response_class=HTMLResponse,)
async def tracking(request: Request, bodypartSelect: str):    
    context = {"request": request, "bodypartSelect": bodypartSelect}
    parts = str(bodypartSelect)


    if data.count(parts)>0:
        print("Parts exist")
    elif bodypartSelect == "Choose...":
        print("bad choice")
    else:
        data.append(bodypartSelect)
        print(data)
        
        return templates.TemplateResponse("tracking-container.html", context)



@app.get("/addexcercise/{bodypartSelect}", response_class=HTMLResponse)
async def addexcercise(request: Request, excerciseName: str, bodypartSelect: str):

    #check if excercise exist in workout - to prevent adding the same excercise
    exist = False
    for part, ex in workout.workout_data.items():
        if part == bodypartSelect:
            for ex in ex:
                if 'exerciseName' in ex:
                    ex_name = ex['exerciseName']
                    print(ex_name)
                    if ex_name == excerciseName:
                        exist = True
                        
                    else:
                        exist = False
    if exist == True:
        print(f'Exercise exist: {ex_name}')
    else:
        workout.add_exercise(bodypartSelect, excerciseName)

        context = {"request": request, "excerciseName": excerciseName, "bodypartSelect": bodypartSelect}
        return templates.TemplateResponse("excercise.html", context)


    # workout.add_exercise(bodypartSelect, excerciseName)
    # print(workout.get_data())

    # context = {"request": request, "excerciseName": excerciseName, "bodypartSelect": bodypartSelect}
    # return templates.TemplateResponse("excercise.html", context)
  



@app.get("/addseries/{bodypartSelect}/{excerciseName}", response_class=HTMLResponse)
async def addexcercise(request: Request, bodypartSelect: str, excerciseName: str):

    num = 0
    
    workout.add_set(bodypartSelect, excerciseName, num)
    print(workout.get_data())
    # print(workout.workout_data)

    context = {"request": request, "series": workout.series_num}
    return templates.TemplateResponse("series.html", context)