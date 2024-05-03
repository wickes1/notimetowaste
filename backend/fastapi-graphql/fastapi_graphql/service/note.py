from fastapi_graphql.model.note import Note
from fastapi_graphql.repository.note import NoteRepository
from fastapi_graphql.schema import NoteInput, NoteType


class NoteService:

    @staticmethod
    async def add_note(note_data: NoteInput) -> NoteType:
        note = Note(
            title=note_data.title,
            description=note_data.description,
        )

        await NoteRepository.create(note)

        return NoteType(id=note.id, title=note.title, description=note.description)

    @staticmethod
    async def get_all_notes() -> list[NoteType]:
        notes = await NoteRepository.get_all()
        return [
            NoteType(id=note.id, title=note.title, description=note.description)
            for note in notes
        ]

    @staticmethod
    async def get_note_by_id(note_id: int) -> NoteType:
        note = await NoteRepository.get_by_id(note_id)
        return NoteType(id=note.id, title=note.title, description=note.description)

    @staticmethod
    async def update_note(note_id: int, note_data: NoteInput) -> str:
        note = Note(
            title=note_data.title,
            description=note_data.description,
        )

        await NoteRepository.update(note_id, note)

        return 'Note updated successfully'

    @staticmethod
    async def delete_note(note_id: int) -> bool:
        await NoteRepository.delete(note_id)
        return True
