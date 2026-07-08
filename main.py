from fastapi import FastAPI, status, HTTPException
from schemas import Announcement, AnnouncementCreate, AnnouncementUpdate, Exercise, ExerciseCreate, ExerciseCompleted, ExerciseCompletedCreate, ExerciseUpdate

from datetime import datetime
app = FastAPI()

next_id = 3
announcements = [
   Announcement(id=1, title="Sunday call time is 8:15AM", message ="please arrive 15 minutes early to church service in honor to God", posted_by="Favour Fri Fon"),

   Announcement(id=2, title="New song added", message="Way maker by sinach is now in the song library with lyrics", posted_by="Asantewa")
]


exe_id = 6
completions = []
exercises = [
    
        Exercise(id=1, title="Morning Vocal Warm-up", description="Gentle sirens and lip trills to open the voice before rehearsal. Follow along with the director.", video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", posted_by="Favour"),
    
        Exercise(id=2, title="Lip trills & breath support", description="Loosen the lips and engage breath support before scales.", video_url=None, posted_by="Keturah"),
    
    
        Exercise(id=3, title="Scales & sirens", description="Run major scales up and down, followed by pitch sirens to smooth register breaks.", video_url="https://www.youtube.com/watch?v=3JZ_D3ELwOQ", posted_by="Jude"),
    
    
        Exercise(id=4, title="Breath Control Drill", description="Sustained 'ssss' and 'shhh' exhales to build breath control and diaphragm strength.", video_url="https://www.youtube.com/watch?v=eY52Zsg-KVI", posted_by="isabela"),
    
    
        Exercise(id=5, title="Evening Cool-down", description="Gentle humming and descending scales to relax the voice after rehearsal.", video_url="https://www.youtube.com/watch?v=2Vv-BfVoq4g", posted_by="Caleb")
    
]


@app.get("/")
def get_root():
    return " Welcome to Harmoni"

@app.get("/announcements")
def get_all_announcements():
    return announcements

@app.get("/announcements/{id}")
def get_announcement_by_id(id:int):
    for announcement in announcements:
        if announcement.id == id:
            return announcement
    # if we get here no announcement was found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} not found")


@app.post("/announcements", status_code=status.HTTP_201_CREATED)
def create_announcement(announcement:AnnouncementCreate) -> Announcement:
    # this announcement.model_dump() method is used to convert the AnnouncementCreate object into a dictionary, which is then unpacked into the Announcement constructor using the ** operator. This allows us to create a new Announcement object with the same attributes as the AnnouncementCreate object.

    #announcement.model_dump() turns the AnnouncementCreate into a plain dict of {title, message, posted_by}. Passing that into Announcement(**...) builds a real Announcement, which fills in post_date itself since it wasn't given one. That new object — not the input, not the whole list — is what gets stored and returned
    global next_id
    new_announcement = Announcement(id=next_id, **announcement.model_dump())
    announcements.append(new_announcement)
    next_id += 1
    return new_announcement

@app.put("/announcements/{id}")
def update_entire_announcement(id:int,announcement:AnnouncementCreate):
    # enumerate() gives us both the index and the item while looping.
    # we need the index to actually overwrite the slot in the list below -
    # just looping over the items (like before) only gets us a copy, not a way back in.
    for index, existing_announcement in enumerate(announcements):
        if existing_announcement.id == id:
            # reuse the original post_date instead of letting default_factory
            # generate a new "now" - editing a typo shouldn't change when it was posted
            updated_announcement = Announcement(id=id, post_date=existing_announcement.post_date, **announcement.model_dump())
            announcements[index] = updated_announcement  # this is the line that was missing: save it back into the list
            return updated_announcement
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} not found")



@app.patch("/announcements/{id}")
def update_announcement_partially(id:int, announcement:AnnouncementUpdate):
    for index, existing_announcement in enumerate(announcements):
        if existing_announcement.id == id:
            # exclude_unset=True only includes fields the client actually put in the
            # request body. without it, every field the client left out would show up
            # as None, and we'd wipe out real data with None on every partial edit.
            fields_sent_by_client = announcement.model_dump(exclude_unset=True)
            # model_copy(update=...) takes the existing announcement (id, post_date,
            # and all fields untouched) and overwrites only the keys we pass in -
            # exactly the "leave everything else alone" behavior PATCH is supposed to have.
            updated_announcement = existing_announcement.model_copy(update=fields_sent_by_client)
            announcements[index] = updated_announcement
            return updated_announcement
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} not found")

@app.delete("/announcements/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(id:int):
    for announcement in announcements:
        if announcement.id == id:
            announcements.remove(announcement)
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} not found")



############################## EXERCISES  ######################

@app.get("/exercises", status_code=status.HTTP_200_OK)
def get_all_exercises():
    return exercises

@app.get("/exercises/{id}", status_code=status.HTTP_200_OK)
def get_exercise_by_id(id:int): 
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")

@app.post("/exercises", status_code=status.HTTP_201_CREATED)
def create_exercise(exercise:ExerciseCreate):
    global exe_id
    new_exercise = Exercise(id=exe_id, **exercise.model_dump())
    exercises.append(new_exercise)
    exe_id += 1
    return new_exercise


@app.put("/exercises/{id}")
def update_exercise(id:int, exercise:ExerciseCreate):
    for index, existing_exercise in enumerate(exercises):
        if existing_exercise.id == id:
            updated_exercise = Exercise(id=id, **exercise.model_dump())
            exercises[index] = updated_exercise
            return updated_exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")

@app.delete("/exercises/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(id:int): 
    for exercise in exercises:
        if exercise.id == id:
            exercises.remove(exercise)
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")

@app.patch("/exercises/{id}")
def update_exercise_partially(id:int, exercise:ExerciseUpdate):
    for index, existing_exercise in enumerate(exercises):
        if existing_exercise.id == id:
            fields_sent_by_client = exercise.model_dump(exclude_unset=True)
            # model_copy(update=...) takes the existing exercise (id, post_date,
            # and all fields untouched) and overwrites only the keys we pass in -
            # exactly the "leave everything else alone" behavior PATCH is supposed to have.
            updated_exercise = existing_exercise.model_copy(update=fields_sent_by_client)
            exercises[index] = updated_exercise
            return updated_exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"exercise with id {id} not found")

@app.post("/exercises/{id}/complete", status_code=status.HTTP_201_CREATED)
def mark_exercise_complete(id:int, completion:ExerciseCompletedCreate) -> ExerciseCompleted:
    # same lookup pattern as get_exercise_by_id - confirms the exercise exists
    # before we let anyone record a completion against it
    for exercise in exercises:
        if exercise.id == id:
            new_completion = ExerciseCompleted(exercise_id=id, singer_name=completion.singer_name)
            completions.append(new_completion)
            return new_completion
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")

@app.get("/exercises/completed/{singer_name}")
def get_todays_completions(singer_name:str) -> list[ExerciseCompleted]:
    today = datetime.now().date()  # .date() drops the time, leaving just the calendar day (e.g. 2026-07-08)
    todays_completions = []
    for completion in completions:
        # completion.completed_at.date() also drops its time, so this compares "same day",
        # not "same exact second" - a completion from this morning still counts as today
        if completion.singer_name == singer_name and completion.completed_at.date() == today:
            todays_completions.append(completion)
    return todays_completions
