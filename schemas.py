from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


#we needed two classes here because we want to have a separate model for creating announcements (AnnouncementCreate) that doesn't include the post_date field, which is automatically generated when an announcement is created. The Announcement model includes the post_date field, which is set to the current date and time when an announcement is created. This allows us to have a clear separation between the data that is required to create an announcement and the data that is returned when an announcement is retrieved.
class AnnouncementCreate(BaseModel):
    title: str
    message: str
    posted_by: str

# every field is Optional with a None default so a PATCH request can send
# only the fields it wants to change - anything left out just stays None here,
# which the endpoint uses to know "the client didn't touch this one"
class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    posted_by: Optional[str] = None

class Announcement(BaseModel):
    id :int
    title : str 
    message : str
    posted_by: str 
    post_date : datetime = Field(default_factory=datetime.now, description="The date and time when the announcement was posted")

    
   
    
    