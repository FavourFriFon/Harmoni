from datetime import datetime
from pydantic import BaseModel
class announcement(BaseModel):
    title : str 
    message : str
    posted_by: str 
    post_date : datetime

    
    """ def __init__(self, title:str,message:str,posted_by:str,post_date:datetime):
        self.title = title
        self.message =message
        self.posted_by=posted_by
        self.post_date=post_date """
   
    
    