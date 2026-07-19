from pydantic import BaseModel, ConfigDict, Field


class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class NoteReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    user_id: int


class NoteUpdateSchema(BaseModel):
    title: str
    content: str


class NotePatchSchema(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)
