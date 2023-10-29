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
        # # sprawdzic czy jak usune ponizszy warunek zadziala prawidlowo - bo dodaje tylko inputy w js
        # if existing_part is not None:
        #     existing_exercise = next((ex for ex in existing_part if ex["exerciseName"] == exercise_name), None)

        # if existing_exercise is None:
        #     existing_part.append({"exerciseName": exercise_name, "sets": []})

        if existing_part is not None:
            existing_part.append({"exerciseName": exercise_name, "sets": []})


    def add_set(self, body_part, exercise_name, repetitions, weight):
        existing_part = self.workout_data.get(body_part)
        if existing_part is not None:
            existing_exercise = next((ex for ex in existing_part if ex["exerciseName"] == exercise_name), None)
            if existing_exercise is not None:
                if "sets" not in existing_exercise:
                    existing_exercise["sets"] = []

                series_count = len(existing_exercise["sets"]) + 1
                self.series_num =series_count
                existing_exercise["sets"].append({"set": series_count, "repetitions": repetitions, "weight": weight})
            else:
                self.add_exercise(body_part, exercise_name)
                self.add_set(body_part, exercise_name, repetitions, weight)
        else:
            self.add_exercise(body_part, exercise_name)
            self.add_set(body_part, exercise_name, repetitions, weight)


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
    def exercise_exists(data, body_part, exercise_name):
        if body_part in data:
            existing_part = data[body_part]
            for exercise in existing_part:
                if exercise['exerciseName'] == exercise_name:
                    return True
        return False
    
    # if exercise exist in specific bodypart -- don't add
    # if not exist - add new exercise
    if exercise_exists(workout.workout_data, bodypartSelect, excerciseName):
        print(f'Exercise exist: {excerciseName}')
    else:
        workout.add_exercise(bodypartSelect, excerciseName)
        print(workout.workout_data)
        context = {"request": request, "excerciseName": excerciseName, "bodypartSelect": bodypartSelect}
        return templates.TemplateResponse("excercise.html", context)




@app.get("/addseries/{bodypartSelect}/{excerciseName}", response_class=HTMLResponse)
async def addexcercise(request: Request, bodypartSelect: str, excerciseName: str):

    num = 0
    weight = 0
    workout.add_set(bodypartSelect, excerciseName, num, weight)
    print(workout.workout_data)

    context = {"request": request, "series": workout.series_num, "excerciseName": excerciseName}
    return templates.TemplateResponse("series.html", context)



@app.delete("/deleteexercise/{excerciseName}", status_code=200)
async def delete_exercise(excerciseName: str):
    print(excerciseName)
    for part, exc in workout.workout_data.items():
        for ex in exc:
            if ex['exerciseName'] == excerciseName:
                del ex['exerciseName']
                del ex['sets']
    workout.workout_data = {body_part: [exercise for exercise in exercises if exercise] for body_part, exercises in workout.workout_data.items()}
    print(workout.workout_data)
    context = {"excerciseName": excerciseName}
    return context



@app.put("/edit/{bodypartSelect}/{excerciseName}/{exNew}",  status_code=200)
async def edit(excerciseName: str, bodypartSelect: str, exNew: str):
    print(bodypartSelect+" "+ excerciseName+" "+ exNew)


    for part, exercises in workout.workout_data.items():
        if part == bodypartSelect:
            for ex in exercises:
                if ex['exerciseName'] == excerciseName:
                    new_exercise = {
                    'exerciseName': exNew,
                    'sets': ex['sets']
                    }
                    exercises.append(new_exercise)
                    exercises.remove(ex)
                    # ex['exerciseName'] = exNew

    print(workout.workout_data)
    context = {"exNew": exNew}
    return context


@app.delete("/deleteseries/{bodypartSelect}/{excerciseName}/{series}")
def delete_series(excerciseName: str, bodypartSelect: str, series: int):
    
    for exercise in workout.workout_data['Chest']:
    sets = exercise['sets']
    updated_sets = [s for s in sets if s['set'] != set_to_remove]
    exercise['sets'] = updated_sets

    # Zaktualizuj numery zbiorów, aby były po kolei
    for i, exercise in enumerate(data['Chest']):
    sets = exercise['sets']
    for j, set in enumerate(sets):
        set['set'] = j + 1


    context = {"series": series}
    return context