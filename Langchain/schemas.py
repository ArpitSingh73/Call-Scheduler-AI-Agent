from pydantic import BaseModel

class Schema1(BaseModel):
    title: str
    headline: str

class Schema2(BaseModel):
    title: str
    headline: str 
    content: str   



     