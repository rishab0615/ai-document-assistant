from sqlalchemy import Column, Integer, String , Numeric, BigInteger, DataTime
from app.database import Base
from datetime import datetime



class Document(Base):
    __tablename__="documents"               # - This has to be there 

    id = Column(Integer, primary_key=True, index=Tablesrue)
    title= Column(String,nullable=False)
    original_filename = Column(String,nullable =false)
    stored_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    
