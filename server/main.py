from collections import defaultdict
from math import sqrt
import random
from random import sample
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, constr
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

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
@app.get("/populate-dummy-data/")
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
        Provider(name="Dr. Helen", specialization="Counselor", location="Los Angeles", gender="Female", language="English", cultural_background="Latino"),
        Provider(name="Dr. Ian", specialization="Psychologist", location="Chicago", gender="Male", language="French", cultural_background="Canadian"),
        Provider(name="Dr. Jane", specialization="Psychiatrist", location="New York", gender="Female", language="English", cultural_background="American")
    
    ]

    # Add some dummy clients
    clients = [
        Client(name="John Doe", need="Anxiety", location="New York", gender="Male", language="English", cultural_background="American", preferred_gender="Female", preferred_cultural_background="American"),
        Client(name="Jane Smith", need="Depression", location="Los Angeles", gender="Female", language="Spanish", cultural_background="Latino", preferred_gender="Male", preferred_cultural_background="Latino"),
        Client(name="Michael Lee", need="Stress", location="San Francisco", gender="Male", language="Mandarin", cultural_background="Chinese", preferred_gender="Female", preferred_cultural_background="Chinese"),
        Client(name="Emily Davis", need="Grief", location="Miami", gender="Female", language="English", cultural_background="American", preferred_gender="Male", preferred_cultural_background="Cuban"),
        Client(name="Laura Garcia", need="Relationship Issues", location="Houston", gender="Female", language="Spanish", cultural_background="Mexican", preferred_gender="Male", preferred_cultural_background="Mexican"),
        Client(name="David Nguyen", need="Trauma", location="Chicago", gender="Male", language="English", cultural_background="Canadian", preferred_gender="Female", preferred_cultural_background="Canadian"),
        Client(name="Sarah Johnson", need="Anxiety", location="New York", gender="Female", language="English", cultural_background="American", preferred_gender="Male", preferred_cultural_background="American"),
        Client(name="Robert Wilson", need="Depression", location="Los Angeles", gender="Male", language="Spanish", cultural_background="Latino", preferred_gender="Female", preferred_cultural_background="Latino"),
        Client(name="Jessica Taylor", need="Stress", location="San Francisco", gender="Female", language="Mandarin", cultural_background="Chinese", preferred_gender="Male", preferred_cultural_background="Chinese"),
        Client(name="Michael Brown", need="Grief", location="Miami", gender="Male", language="English", cultural_background="American", preferred_gender="Female", preferred_cultural_background="Cuban")
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

# Calculate scores based on content filtering
def content_based_score(client: Client, provider: Provider) -> float:
    score = 0
    
    if provider.location == client.location:
        score += 50  # Weight for matching location
    if provider.gender == client.preferred_gender:
        score += 30  # Weight for matching gender
    if provider.cultural_background == client.preferred_cultural_background:
        score += 20  # Weight for matching cultural background

    return score

# Calculate scores based on collaborative filtering
def collaborative_score(client_id: int, provider_id: int, db: Session) -> float:
    mappings = db.query(ClientProviderMapping).all()
    client_ratings = defaultdict(dict)

    # Populate client ratings for providers
    for mapping in mappings:
        client_ratings[mapping.client_id][mapping.provider_id] = mapping.rating

    # Calculate collaborative score based on similar clients
    target_client_ratings = client_ratings[client_id]
    score = 0
    count = 0

    for other_client_id, ratings in client_ratings.items():
        if other_client_id == client_id:
            continue
        similarity = calculate_pearson_correlation(target_client_ratings, ratings)
        if similarity > 0:
            score += similarity * ratings.get(provider_id, 0)
            count += 1

    return (score / count) if count > 0 else 0

# Combine content and collaborative scores
def combined_score(client: Client, provider: Provider, db: Session) -> float:
    content_score = content_based_score(client, provider)
    collaborative_score_value = collaborative_score(client.id, provider.id, db)
    
    # Normalize collaborative score to be out of 100
    collaborative_score_normalized = (collaborative_score_value / 5) * 100  # Assuming ratings are out of 5
    total_score = (content_score * 0.6) + (collaborative_score_normalized * 0.4)  # Weighted average

    return min(total_score, 100)  # Ensure score is capped at 100

# Get recommendations for a client
def get_recommendations(client_id: int, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    providers = db.query(Provider).all()
    
    provider_scores = []
    
    for provider in providers:
        score = combined_score(client, provider, db)
        provider_scores.append((provider, score))

    # Sort providers by score in descending order
    provider_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 5 providers with scores
    top_providers = provider_scores[:5]
    
    return {
        "recommendations": [
            {
                "id": provider.id,
                "name": provider.name,
                "specialization": provider.specialization,
                "location": provider.location,
                "gender": provider.gender,
                "language": provider.language,
                "cultural_background": provider.cultural_background,
                "score": score
            }
            for provider, score in top_providers
        ]
    }

# Pearson correlation for similarity between two clients' ratings
def calculate_pearson_correlation(ratings1, ratings2):
    common_providers = set(ratings1.keys()) & set(ratings2.keys())

    if len(common_providers) == 0:
        return 0  # No common providers, similarity is 0

    sum1, sum2, sum1_sq, sum2_sq, sum_products = 0, 0, 0, 0, 0
    for provider_id in common_providers:
        rating1 = ratings1[provider_id]
        rating2 = ratings2[provider_id]
        sum1 += rating1
        sum2 += rating2
        sum1_sq += rating1 ** 2
        sum2_sq += rating2 ** 2
        sum_products += rating1 * rating2

    numerator = sum_products - (sum1 * sum2 / len(common_providers))
    denominator = sqrt((sum1_sq - sum1 ** 2 / len(common_providers)) * (sum2_sq - sum2 ** 2 / len(common_providers)))

    return numerator / denominator if denominator != 0 else 0

# Recommendation API
@app.get("/recommend/{client_id}")
def recommend(client_id: int, db: Session = Depends(get_db)):
    recommendations = get_recommendations(client_id, db)
    return recommendations

# Basic root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the SQLite-based recommender system API!"}
