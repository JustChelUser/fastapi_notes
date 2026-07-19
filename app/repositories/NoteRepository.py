from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Note


class NoteRepository():
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_by_user(self, user_id: int) -> list[Note]:
        statement = select(Note).where(Note.user_id == user_id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, note_id: int) -> Note | None:
        statement = select(Note).where(Note.id == note_id)
        return self.db.execute(statement).scalar_one_or_none()

    def delete(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()

    def create(self, title: str, content: str, user_id: int) -> Note:
        note = Note(title=title, content=content, user_id=user_id)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: Note, title: str, content: str) -> Note:
        note.title = title
        note.content = content
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def patch(self, note: Note, update_dict: dict) -> Note:
        for key, value in update_dict.items():
            setattr(note, key, value)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
