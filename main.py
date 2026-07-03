from fastapi import FastAPI
from models import announcement
from datetime import datetime
app = FastAPI()


announcements = [
    announcement(title="Sunday call time is 8:15AM", message ="please arrive 15 minutes early to church service in honor to God", posted_by="Favour Fri Fon",post_date= datetime(2026,7,4,0,0)),
    announcement(title="New song added", message="Way maker by sinach is now in the song library with lyrics", posted_by="Asantewa", post_date=datetime(2026,7,4,12,50))
]

@app.get("/")
def get_root():
    return " Welcome to Harmoni"

@app.get("/announcements")
def get_announcements():
    return announcements