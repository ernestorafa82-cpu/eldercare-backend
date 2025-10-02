from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session
from db import init_db, get_session
from models import Elder, Event

app = FastAPI(title="ElderCare API")
# importa el middleware al inicio del archivo (si no lo tienes)
from fastapi.middleware.cors import CORSMiddleware

# después de crear app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next dev
        "http://localhost:3002",  # en tus capturas salía 3002
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/elders", response_model=dict)
def create_elder(
    full_name: str,
    phone: str | None = None,
    address: str | None = None,
    session: Session = Depends(get_session),
):
    elder = Elder(full_name=full_name, phone=phone, address=address)
    session.add(elder)
    session.commit()
    session.refresh(elder)
    return {"id": elder.id}

@app.post("/elders/{elder_id}/events", response_model=dict)
def add_event(
    elder_id: int,
    type: str,
    payload: str | None = None,
    session: Session = Depends(get_session),
):
    if not session.get(Elder, elder_id):
        raise HTTPException(404, "Elder not found")

    ev = Event(elder_id=elder_id, type=type, payload=payload)
    session.add(ev)
    session.commit()
    session.refresh(ev)
    return {"id": ev.id, "created_at": ev.created_at.isoformat()}

@app.get("/elders/{elder_id}/timeline", response_model=List[dict])
def timeline(
    elder_id: int,
    limit: int = Query(3, ge=1, le=100),
    type: Optional[str] = None,
    session: Session = Depends(get_session),
):
    if not session.get(Elder, elder_id):
        raise HTTPException(404, "Elder not found")

    q = select(Event).where(Event.elder_id == elder_id)
    if type:
        q = q.where(Event.type == type)
    q = q.order_by(Event.created_at.desc()).limit(limit)

    events = session.exec(q).all()
    return [
        {"id": e.id, "type": e.type, "payload": e.payload, "created_at": e.created_at.isoformat()}
        for e in events
    ]
