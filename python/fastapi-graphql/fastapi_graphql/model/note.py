from typing import Optional
from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    __tablename__ = "note"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str
    description: str
