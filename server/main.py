from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, constr
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
# API to populate dummy data for testing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD
import numpy as np


# FastAPI app
app = FastAPI()

# SQLite Database connection
DATABASE_URL = "sqlite:///./recommender.db"

# SQLite-specific configuration (check_same_thread=False)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    language = Column(String(50), nullable=True)
    cultural_background = Column(String(100), nullable=True)

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    need = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    language = Column(String(50), nullable=True)
    cultural_background = Column(String(100), nullable=True)
    preferred_gender = Column(String(10), nullable=True) 
    preferred_cultural_background = Column(String(100), nullable=True)

class ClientProviderMapping(Base):
    __tablename__ = 'client_provider_mapping'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=True)  # Add rating (1-5 scale)
    
    client = relationship("Client")
    provider = relationship("Provider")


# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models (For Validation and Parsing)
class ProviderCreate(BaseModel):
    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String(100), nullable=False)
    # specialization = Column(String(100), nullable=False)
    # location = Column(String(100), nullable=False)
    # gender = Column(String(10), nullable=True)
    # language = Column(String(50), nullable=True)
    # cultural_background = Column(String(100), nullable=True)
    name: constr(min_length=1, max_length=100)
    specialization: constr(min_length=1, max_length=100)
    location: constr(min_length=1, max_length=100)

class ClientCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    need: constr(min_length=1, max_length=100)
    location: constr(min_length=1, max_length=100)

class ClientProviderMappingCreate(BaseModel):
    client_id: int = Field(..., gt=0)
    provider_id: int = Field(..., gt=0)
    rating: int = Field(None, ge=1, le=5)  # Optional rating (1-5 scale)


# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API to add a provider
@app.post("/providers/", response_model=ProviderCreate)
def add_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    new_provider = Provider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

# API to add a client
@app.post("/clients/", response_model=ClientCreate)
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# API to add a client-provider mapping
@app.post("/client-provider-mapping/", response_model=ClientProviderMappingCreate)
def add_client_provider_mapping(mapping: ClientProviderMappingCreate, db: Session = Depends(get_db)):
    # Check if client and provider exist
    client = db.query(Client).filter(Client.id == mapping.client_id).first()
    provider = db.query(Provider).filter(Provider.id == mapping.provider_id).first()

    if not client or not provider:
        raise HTTPException(status_code=404, detail="Client or Provider not found.")
    
    new_mapping = ClientProviderMapping(**mapping.dict())
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    
    return new_mapping



# API to populate dummy data for testing
@app.post("/populate-dummy-data/")
def populate_dummy_data(db: Session = Depends(get_db)):
    # Add some dummy providers
    providers = [
        Provider(name="Dr. Alice", specialization="Psychologist", location="New York", gender="Female", language="English", cultural_background="American"),
        Provider(name="Dr. Bob", specialization="Therapist", location="Los Angeles", gender="Male", language="Spanish", cultural_background="Latino"),
        Provider(name="Dr. Charlie", specialization="Counselor", location="Chicago", gender="Non-binary", language="French", cultural_background="Canadian"),
        Provider(name="Dr. Diana", specialization="Psychiatrist", location="Miami", gender="Female", language="English", cultural_background="Cuban"),
        Provider(name="Dr. Edward", specialization="Life Coach", location="Houston", gender="Male", language="English", cultural_background="British"),
        Provider(name="Dr. Fiona", specialization="Psychologist", location="New York", gender="Female", language="Spanish", cultural_background="Mexican"),
        Provider(name="Dr. George", specialization="Therapist", location="San Francisco", gender="Male", language="Mandarin", cultural_background="Chinese"),
    ]

    # Add some dummy clients
    clients = [
        Client(name="John Doe", need="Anxiety", location="New York", gender="Male", language="English", cultural_background="American", preferred_gender="Female", preferred_cultural_background="American"),
        Client(name="Jane Smith", need="Depression", location="Los Angeles", gender="Female", language="Spanish", cultural_background="Latino", preferred_gender="Male", preferred_cultural_background="Latino"),
        Client(name="Michael Lee", need="Stress", location="San Francisco", gender="Male", language="Mandarin", cultural_background="Chinese", preferred_gender="Female", preferred_cultural_background="Chinese"),
        Client(name="Emily Davis", need="Grief", location="Miami", gender="Female", language="English", cultural_background="American", preferred_gender="Male", preferred_cultural_background="Cuban"),
        Client(name="Laura Garcia", need="Relationship Issues", location="Houston", gender="Female", language="Spanish", cultural_background="Mexican", preferred_gender="Male", preferred_cultural_background="Mexican"),
    ]
    mappings = [
        ClientProviderMapping(client_id=1, provider_id=1, rating=5),
        ClientProviderMapping(client_id=1, provider_id=2, rating=3),
        ClientProviderMapping(client_id=2, provider_id=2, rating=4),
        ClientProviderMapping(client_id=2, provider_id=3, rating=5),
    ]
    # Insert into the database
    db.add_all(providers)
    db.add_all(clients)
    db.add_all(mappings)
    db.commit()
    
    return {"message": "Dummy data added successfully."}


# Basic root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the SQLite-based recommender system API!"}
