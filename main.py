from fastapi import FastAPI, status, HTTPException
from schemas import Announcement, AnnouncementCreate, AnnouncementUpdate
from datetime import datetime
app = FastAPI()

next_id = 3
announcements = [
   Announcement(id=1, title="Sunday call time is 8:15AM", message ="please arrive 15 minutes early to church service in honor to God", posted_by="Favour Fri Fon"),

   Announcement(id=2, title="New song added", message="Way maker by sinach is now in the song library with lyrics", posted_by="Asantewa")
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


