from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #If the user does not provide a value, de default is True
    #rating: Optional[int] = None #Optional field with a default value of none/null

class PostCreate(PostBase):
    pass

