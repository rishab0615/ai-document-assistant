from sqlalchemy import Column, Integer, String , Numeric, BigInteger, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime
from sqlalchemy.sql import func


class Document(Base):
    __tablename__="documents"               # - This has to be there 

    id = Column(Integer, primary_key=True, index=True)
    extracted_text = Column(Text)                   # - Text is designed for larger text 5 or 500000
    user_id = Column(Integer, ForeignKey("users.id"))
    original_filename = Column(String,nullable =False)
    stored_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    
class User(Base):
    __tablename__="users" 

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__="chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    document_id =  Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role =  Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False 
)




