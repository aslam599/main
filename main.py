from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI(
title="Aplikasi API Saya",
    description="API sederhana yang dibangun dengan FastAPI",
    version="0.1.0",
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Selamat Datang</title>
    </head>
    <body>
        <h1>Selamat datang di aplikasi FastAPI saya!</h1>
        <p>Ini adalah halaman utama.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)



# Informasi koneksi database
DATABASE_URL = "sqlite:///./mydatabase.db"  # Contoh SQLite, ganti dengan koneksi database Anda

# Membuat engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Membuat sesi database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mendefinisikan model database menggunakan SQLAlchemy ORM
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

# Membuat database jika belum ada
Base.metadata.create_all(bind=engine)

# Dependency untuk mendapatkan sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model Pydantic untuk response data
class ItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Membuat instance FastAPI
app = FastAPI()

# Endpoint untuk mendapatkan semua item
@app.get("/items/", response_model=List[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

# Contoh endpoint lain untuk mendapatkan item berdasarkan ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    return item