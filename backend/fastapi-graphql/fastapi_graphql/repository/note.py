from sqlalchemy import select
from fastapi_graphql.model.note import Note
from fastapi_graphql.config import db
from sqlalchemy import update as sql_update, delete as sql_delete


class NoteRepository:

    @staticmethod
    async def create(note_data: Note):
        async with db as session:
            async with session.begin():
                session.add(note_data)
            await db.commit_rollback()

    @staticmethod
    async def get_by_id(note_id: int) -> Note:
        async with db as session:
            stmt = select(Note).where(Note.id == note_id)
            result = await session.execute(stmt)
            note = result.scalars().first()
            return note

    @staticmethod
    async def get_all() -> list[Note]:
        async with db as session:
            stmt = select(Note)
            result = await session.execute(stmt)
            notes = result.scalars().all()
            return notes

    @staticmethod
    async def update(note_id: int, note_data: Note):
        async with db as session:
            stmt = select(Note).where(Note.id == note_id)
            result = await session.execute(stmt)

            note = result.scalars().first()
            note.title = note_data.title
            note.description = note_data.description

            query = (
                sql_update(Note).where(Note.id == note_id).values(**note.model_dump())
            )

            await session.execute(query)
            await db.commit_rollback()

    @staticmethod
    async def delete(note_id: int):
        async with db as session:
            query = sql_delete(Note).where(Note.id == note_id)

            await session.execute(query)
            await db.commit_rollback()
