from pydantic import BaseModel
    

class DocumentCreate(BaseModel):
    title: str
    original_filename: str
    stored_filename: str
    content_type: str
    file_size: int

class DocumentResponse(BaseModel):
    id:int
    title: str
    original_filename:str
    stored_filename:str
    content_type:str
    file_size:int
    # model_config = ConfigDict(from_attributes=True)    


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # model_config = ConfigDict(from_attributes=True)    