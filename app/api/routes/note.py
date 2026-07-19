from fastapi import APIRouter
from fastapi import status
from fastapi.params import Depends

from app.api.dependencies import get_note_service, get_current_user
from app.models import User
from app.schemas.Note import NoteReadSchema, NoteCreateSchema, NoteUpdateSchema, NotePatchSchema
from app.services.NoteService import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteReadSchema, status_code=status.HTTP_201_CREATED)
def create_new_note(note_data: NoteCreateSchema,
                    service: NoteService = Depends(get_note_service),
                    current_user: User = Depends(get_current_user)):
    return service.create_note(note_data=note_data, user_id=current_user.id)


@router.get("/", response_model=list[NoteReadSchema])
def get_my_notes(service: NoteService = Depends(get_note_service),
                 current_user: User = Depends(get_current_user)):
    return service.get_user_notes(user_id=current_user.id)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_note(note_id: int,
                   service: NoteService = Depends(get_note_service),
                   current_user: User = Depends(get_current_user)):
    service.delete_note(note_id=note_id, user_id=current_user.id)
    return None


@router.put("/{note_id}", response_model=NoteReadSchema)
def update_my_note(note_id: int,
                   note_data: NoteUpdateSchema,
                   service: NoteService = Depends(get_note_service),
                   current_user: User = Depends(get_current_user)):
    return service.update_note(
        note_id=note_id,
        user_id=current_user.id,
        update_data=note_data,
    )


@router.patch("/{note_id}", response_model=NoteReadSchema)
def patch_my_note(
        note_id: int,
        note_data: NotePatchSchema,
        service: NoteService = Depends(get_note_service),
        current_user: User = Depends(get_current_user)
):
    return service.patch_note(
        note_id=note_id,
        user_id=current_user.id,
        patch_data=note_data
    )
