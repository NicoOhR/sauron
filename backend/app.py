from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional
import os 

try:
    from dotenv import load_dotenv 
    load_dotenv()
except:
    pass 

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    throughput: float = Field(default=0.0)
    latency: float = Field(default=0.0)
    cost: float = Field(default=0.0)
    
class Node(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    throughput: float = Field(default=0.0)
    latency: float = Field(default=0.0)
    cost: float = Field(default=0.0)
    
class Vertex(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inputNodeId: int = Field(index=True)
    topicId: int = Field(index=True)
    outputNodeId: int = Field(index=True)

sqlite_url = os.environ.get("POSTGRES_URL")

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/nodes/")
def create_hero(hero: Node, session: SessionDep) -> Node:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/nodes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Node]:
    heroes = session.exec(select(Node).offset(offset).limit(limit)).all()
    return heroes

@app.post("/topics/")
def create_hero(hero: Topic, session: SessionDep) -> Topic:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/topics/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Topic]:
    heroes = session.exec(select(Topic).offset(offset).limit(limit)).all()
    return heroes

@app.post("/vertices/")
def create_hero(hero: Vertex, session: SessionDep) -> Vertex:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/vertices/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Vertex]:
    heroes = session.exec(select(Vertex).offset(offset).limit(limit)).all()
    return heroes
