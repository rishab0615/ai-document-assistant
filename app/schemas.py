from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):

    original_filename: str
    stored_filename: str
    content_type: str
    file_size: int

class DocumentResponse(BaseModel):
    id:int

    original_filename:str
    stored_filename:str
    content_type:str
    file_size:int


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # model_config = ConfigDict(from_attributes=True)    

class UserLogin(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class AIQuestion(BaseModel):
    document_id: int
    question: str

class AIResponse(BaseModel):
    answer: str



class ChatMessageResponse(BaseModel):
    id: int
    document_id: int
    user_id: int
    role: str
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


