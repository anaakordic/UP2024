from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Create a base class using the updated import path
Base = declarative_base()

class Autori(Base):
    __tablename__ = 'Autori'
    autor_id = Column(Integer, primary_key=True, autoincrement=True)
    ime = Column(String(50), nullable=False)
    prezime = Column(String(50), nullable=False)
    knjige = relationship("Knjige", back_populates="autor")

class Zanrovi(Base):
    __tablename__ = 'Zanrovi'
    zanr_id = Column(Integer, primary_key=True, autoincrement=True)
    naziv = Column(String(50), nullable=False)
    knjige = relationship("Knjige", back_populates="zanr")

class Izdavaci(Base):
    __tablename__ = 'Izdavaci'
    izdavac_id = Column(Integer, primary_key=True, autoincrement=True)
    naziv = Column(String(100), nullable=False)
    adresa = Column(String(255))
    knjige = relationship("Knjige", back_populates="izdavac")

class Knjige(Base):
    __tablename__ = 'Knjige'
    knjiga_id = Column(Integer, primary_key=True, autoincrement=True)
    naslov = Column(String(255), nullable=False)
    autor_id = Column(Integer, ForeignKey('Autori.autor_id'))
    zanr_id = Column(Integer, ForeignKey('Zanrovi.zanr_id'))
    izdavac_id = Column(Integer, ForeignKey('Izdavaci.izdavac_id'))
    godina_izdanja = Column(Integer)
    dostupno = Column(Boolean)
    autor = relationship("Autori", back_populates="knjige")
    zanr = relationship("Zanrovi", back_populates="knjige")
    izdavac = relationship("Izdavaci", back_populates="knjige")


"""class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
"""

class Clanovi(Base):
    __tablename__ = 'Clanovi'

    clan_id = Column(Integer, primary_key=True, autoincrement=True)
    ime = Column(String(50), nullable=False)
    prezime = Column(String(50), nullable=False)
    adresa = Column(String(255))
    broj_telefona = Column(String(15))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
