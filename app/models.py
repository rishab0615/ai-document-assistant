from sqlalchemy import Column, Integer, String , Numeric
from app.database import Base



class Document(Base):
    __tablename__="documents"               # - This has to be there 
    
