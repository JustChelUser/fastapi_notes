from pydantic import BaseModel, ConfigDict, Field


class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=20)


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
