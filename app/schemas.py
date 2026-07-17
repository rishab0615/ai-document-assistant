from pydantic import BaseModel
    

class DocumentCreate(BaseModel):
    title: str
    original_filename: str
    stored_filename: str
    content_type: str
    file_size: int

class DocumentResponse(BaseModel):
    title: str
    id: int