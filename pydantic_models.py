from pydantic import BaseModel, EmailStr


class AutoriBase(BaseModel):
    autor_id: int
    ime: str
    prezime: str

    class Config:
        from_attributes = True

class ZanroviBase(BaseModel):
    zanr_id: int
    naziv: str

    class Config:
        from_attributes = True

class IzdavaciBase(BaseModel):
    izdavac_id: int
    naziv: str
    adresa: str

    class Config:
        from_attributes = True

class KnjigeBase(BaseModel):
    knjiga_id: int
    naslov: str
    autor_id: int
    zanr_id: int
    izdavac_id: int
    godina_izdanja: int
    dostupno: bool
    autor: AutoriBase
    zanr: ZanroviBase
    izdavac: IzdavaciBase

    class Config:
        from_attributes = True


class ClanCreate(BaseModel):
    ime: str
    prezime: str
    adresa: str
    broj_telefona: str
    username: str
    password: str
    email: EmailStr

class ClanDisplay(BaseModel):
    clan_id: int
    ime: str
    prezime: str
    adresa: str
    broj_telefona: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Allows the model to be converted from an ORM model

class ClanLogin(BaseModel):
    username: str
    password: str      


"""class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr"""



from pydantic import BaseModel

class KnjigaCreate(BaseModel):
    naslov: str
    autor_id: int
    zanr_id: int
    izdavac_id: int
    godina_izdanja: int
    dostupno: bool

    class Config:
        from_attributes = True
