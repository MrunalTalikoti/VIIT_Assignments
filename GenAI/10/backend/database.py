# backend/database.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///history.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ImageHistory(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    prompt = Column(String)
    style = Column(String)
    image_path = Column(String)

Base.metadata.create_all(bind=engine)