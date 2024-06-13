from sqlalchemy.orm import Session
from models import Knjige
from schemas import KnjigaCreate

def get_all_knjige(db: Session):
    return db.query(Knjige).all()

def get_knjiga(db: Session, knjiga_id: int):
    return db.query(Knjige).filter(Knjige.knjiga_id == knjiga_id).first()

def create_knjiga(db: Session, knjiga: KnjigaCreate):
    db_knjiga = Knjige(**knjiga.dict())
    db.add(db_knjiga)
    db.commit()
    db.refresh(db_knjiga)
    return db_knjiga

def update_knjiga(db: Session, knjiga_id: int, knjiga_data: dict):
    db.query(Knjige).filter(Knjige.knjiga_id == knjiga_id).update(knjiga_data)
    db.commit()

def delete_knjiga(db: Session, knjiga_id: int):
    db.query(Knjige).filter(Knjige.knjiga_id == knjiga_id).delete()
    db.commit()
