from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from app.repositories.NoteRepository import NoteRepository
from app.schemas.Note import NoteCreateSchema, NoteReadSchema, NoteUpdateSchema, NotePatchSchema


class NoteService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.note_repository = NoteRepository(self.db)

    def create_note(self, note_data: NoteCreateSchema, user_id: int) -> NoteReadSchema:
        new_note = self.note_repository.create(title=note_data.title,
                                               content=note_data.content,
                                               user_id=user_id)
        return NoteReadSchema.model_validate(new_note)

    def get_user_notes(self, user_id: int) -> list[NoteReadSchema]:
        notes = self.note_repository.get_all_by_user(user_id=user_id)
        return [NoteReadSchema.model_validate(note) for note in notes]

    def delete_note(self, note_id: int, user_id: int) -> None:
        note = self.note_repository.get_by_id(note_id=note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заметка не найдена"
            )
        if note.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет прав для удаления этой заметки"

            )
        self.note_repository.delete(note)

    def update_note(self, note_id: int, user_id: int, update_data: NoteUpdateSchema) -> NoteReadSchema:
        note = self.note_repository.get_by_id(note_id=note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заметка не найдена"
            )
        if note.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет прав для удаления этой заметки"

            )
        updated_note = self.note_repository.update(
            note=note,
            title=update_data.title,
            content=update_data.content,
        )
        return NoteReadSchema.model_validate(updated_note)

    def patch_note(self, note_id: int, user_id: int, patch_data: NotePatchSchema) -> NoteReadSchema:
        note = self.note_repository.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Заметка не найдена")
        if note.user_id != user_id:
            raise HTTPException(status_code=403, detail="У вас нет прав для изменения этой заметки")
        update_dict = patch_data.model_dump(exclude_unset=True)
        if not update_dict:
            return NoteReadSchema.model_validate(note)
        patched_note = self.note_repository.patch(note=note, update_dict=update_dict)
        return NoteReadSchema.model_validate(patched_note)
