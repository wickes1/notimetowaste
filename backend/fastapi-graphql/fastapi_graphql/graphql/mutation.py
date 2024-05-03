import strawberry

from fastapi_graphql.schema import NoteInput, NoteType
from fastapi_graphql.service.note import NoteService


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_note(self, note_data: NoteInput) -> NoteType:
        return await NoteService.add_note(note_data)

    @strawberry.mutation
    async def update_note(self, note_id: int, note_data: NoteInput) -> str:
        return await NoteService.update_note(note_id, note_data)

    @strawberry.mutation
    async def delete_note(
        self,
        note_id: int,
    ) -> bool:
        return await NoteService.delete_note(note_id)
