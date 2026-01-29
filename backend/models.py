from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender = Column(String(50))
    receiver = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
