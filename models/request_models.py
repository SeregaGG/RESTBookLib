from pydantic import BaseModel, Field


class RequestBook(BaseModel):
    author: str
    genres: list = Field(default=[])
    title: str

    class Config:
        orm_mode = True


class ResponseBook(RequestBook):
    id: int


class PutRequestBook(BaseModel):
    author: str | None
    genres: list | None
    title: str | None

    class Config:
        orm_mode = True


class PutResponseBook(PutRequestBook):
    id: int
