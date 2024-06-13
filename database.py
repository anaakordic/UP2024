from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection parameters
db_username = "root"
db_password = "lozinka123."
db_host = "127.0.0.1"
db_port = "6306"
db_name = "knjiznica"

# Database connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Creating the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating a SessionLocal class to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()