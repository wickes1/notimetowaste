from typing import List

import strawberry

from fastapi_graphql.schema import NoteType
from fastapi_graphql.service.note import NoteService


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, info) -> str:
        return "Hello, world!"

    @strawberry.field
    def get_all(self, info) -> List[NoteType]:
        return NoteService.get_all_notes()

    @strawberry.field
    async def get_by_id(self, info, note_id: int) -> NoteType:
        return await NoteService.get_note_by_id(note_id)
