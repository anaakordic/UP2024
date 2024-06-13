from pydantic import BaseModel
from datetime import datetime

class KnjigaBase(BaseModel):
    naslov: str
    autor_id: int
    zanr_id: int
    izdavac_id: int
    godina_izdanja: int
    dostupno: bool

class KnjigaCreate(KnjigaBase):
    pass

class Knjiga(KnjigaBase):
    knjiga_id: int

    class Config:
        from_attributes = True
