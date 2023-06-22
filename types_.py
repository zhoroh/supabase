from pydantic import BaseModel
from typing import Optional

class SignUpDto(BaseModel):
    
    email:str
    password:str

class InsertDto(BaseModel):
    id:int
    age:int
    name:str

class UpdateDto(BaseModel):
    age: Optional[int]
    name: Optional[str]