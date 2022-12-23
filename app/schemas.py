from pydantic import BaseModel
from datetime import datetime

# Class for the input of information

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #If the user does not provide a value, de default is True
    #rating: Optional[int] = None #Optional field with a default value of none/null

class PostCreate(PostBase):
    pass


# Class for the response (hides sensitive data, ej.passwords, dates, etc)

class ResponsePost(PostBase): #inherits from PostBase title, content and published
    idPost: int
    created_at: datetime

    class Config: # Needed to be able to send something that is not a dict
        orm_mode = True