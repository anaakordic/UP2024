from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from starlette.status import HTTP_303_SEE_OTHER, HTTP_401_UNAUTHORIZED
import models
import database
import crud
from pydantic_models import ClanDisplay, ClanCreate, ClanLogin, KnjigaCreate, KnjigeBase
from security import verify_password, get_password_hash
from auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/home")
async def get_home(request: Request, db: Session = Depends(get_db)):
    knjige = db.query(models.Knjige).all()
    return templates.TemplateResponse("home.html", {"request": request, "knjige": knjige})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    clan = db.query(models.Clanovi).filter(models.Clanovi.username == form_data.username).first()
    if not clan:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": "User not found"})
    if not verify_password(form_data.password, clan.password):
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": "Incorrect password"})
    
    access_token = create_access_token(data={"sub": clan.username})
    response = RedirectResponse(url="/home", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)  # Set cookie for 30 minutes
    return response

@app.post("/clanovi/register", response_model=ClanDisplay)
def register_clan(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    ime: str = Form(...),
    prezime: str = Form(...),
    adresa: str = Form(None),
    broj_telefona: str = Form(None),
    db: Session = Depends(get_db)):
    existing_clan = db.query(models.Clanovi).filter((models.Clanovi.username == username) | (models.Clanovi.email == email)).first()
    if existing_clan:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(password)
    new_clan = models.Clanovi(username=username, email=email, password=hashed_password, ime=ime, prezime=prezime, adresa=adresa, broj_telefona=broj_telefona)
    db.add(new_clan)
    db.commit()
    db.refresh(new_clan)
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    return response

@app.post("/login")
async def handle_login(request: Request,
                       username: str = Form(...),
                       password: str = Form(...),
                       db: Session = Depends(database.get_db)):
    user = db.query(models.Clanovi).filter(models.Clanovi.username == username).first()
    if user and verify_password(password, user.password):
        # Logic to create a token or session
        response = RedirectResponse(url="/home", status_code=303)
        return response
    else:
        # Redirect back to login with an error message
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"}, status_code=303)

@app.post("/clanovi/login")
def login_clan(clan_login: ClanLogin, db: Session = Depends(get_db)):
    clan = db.query(models.Clanovi).filter(models.Clanovi.username == clan_login.username).first()
    if not clan or not verify_password(clan_login.password, clan.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    return response

@app.get("/", response_model=List[KnjigeBase])
async def read_root(db: Session = Depends(get_db)):
    try:
        knjige = db.query(models.Knjige).all()
        return knjige
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knjige/", response_model=List[KnjigeBase])
def read_all_knjige(db: Session = Depends(get_db)):
    knjige = db.query(models.Knjige).all()
    return knjige

@app.get("/knjige/new")
async def new_knjiga(request: Request, db: Session = Depends(get_db)):
    autori = db.query(models.Autori).all()
    zanrovi = db.query(models.Zanrovi).all()
    izdavaci = db.query(models.Izdavaci).all()
    return templates.TemplateResponse("add_knjiga.html", {
        "request": request,
        "autori": autori,
        "zanrovi": zanrovi,
        "izdavaci": izdavaci
    })

@app.post("/knjige/")
async def create_knjiga(request: Request,
                        naslov: str = Form(...),
                        autor_id: int = Form(...),
                        zanr_id: int = Form(...),
                        izdavac_id: int = Form(...),
                        godina_izdanja: int = Form(...),
                        dostupno: bool = Form(...),
                        db: Session = Depends(get_db)):
    knjiga = KnjigaCreate(
        naslov=naslov,
        autor_id=autor_id,
        zanr_id=zanr_id,
        izdavac_id=izdavac_id,
        godina_izdanja=godina_izdanja,
        dostupno=dostupno
    )
    created_knjiga = crud.create_knjiga(db, knjiga)
    return RedirectResponse(url="/home", status_code=303)

@app.put("/knjige/{knjiga_id}", response_model=KnjigeBase)
def update_knjiga(knjiga_id: int, knjiga: KnjigaCreate, db: Session = Depends(get_db)):
    existing_knjiga = crud.get_knjiga(db, knjiga_id)
    if existing_knjiga is None:
        raise HTTPException(status_code=404, detail="Knjiga not found")
    crud.update_knjiga(db, knjiga_id, knjiga.dict())
    return crud.get_knjiga(db, knjiga_id)

@app.delete("/knjige/{knjiga_id}", response_model=dict)
def delete_knjiga(knjiga_id: int, db: Session = Depends(get_db)):
    db_knjiga = crud.get_knjiga(db, knjiga_id)
    if db_knjiga is None:
        raise HTTPException(status_code=404, detail="Knjiga not found")
    crud.delete_knjiga(db, knjiga_id)
    return {"message": "Knjiga deleted successfully"}

@app.post("/authors/")
async def create_author(request: Request,
                        ime: str = Form(...),
                        prezime: str = Form(...),
                        db: Session = Depends(get_db)):
    autor = models.Autori(ime=ime, prezime=prezime)
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return RedirectResponse(url="/knjige/new", status_code=303)

@app.post("/genres/")
async def create_genre(request: Request,
                       naziv: str = Form(...),
                       db: Session = Depends(get_db)):
    zanr = models.Zanrovi(naziv=naziv)
    db.add(zanr)
    db.commit()
    db.refresh(zanr)
    return RedirectResponse(url="/knjige/new", status_code=303)

@app.post("/publishers/")
async def create_publisher(request: Request,
                           naziv: str = Form(...),
                           adresa: str = Form(None),
                           db: Session = Depends(get_db)):
    izdavac = models.Izdavaci(naziv=naziv, adresa=adresa)
    db.add(izdavac)
    db.commit()
    db.refresh(izdavac)
    return RedirectResponse(url="/knjige/new", status_code=303)


@app.get("/authors/new")
async def new_author(request: Request):
    return templates.TemplateResponse("add_author.html", {"request": request})

@app.get("/genres/new")
async def new_genre(request: Request):
    return templates.TemplateResponse("add_genre.html", {"request": request})

@app.get("/publishers/new")
async def new_publisher(request: Request):
    return templates.TemplateResponse("add_publisher.html", {"request": request})




@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    return response

