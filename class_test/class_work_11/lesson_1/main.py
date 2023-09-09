from fastapi import FastAPI, Path, Query, Depends, HTTPException, status, File, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from db import get_db, Note
import pathlib

app = FastAPI()


class ResponseNoteModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str
    description: str
    done: bool


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Производим запрос
        result = db.execute("SELECT 1").fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/notes")
async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)) -> \
        list[ResponseNoteModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@app.get("/notes/{note_id}", response_model=ResponseNoteModel)
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10),
                    db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note


class NoteModel(BaseModel):
    name: str
    description: str
    done: bool


@app.post("/notes")
async def create_note(note: NoteModel, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}

app.mount("/static", StaticFiles(directory="static"), name="static")