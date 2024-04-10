import strawberry


@strawberry.type
class NoteType:
    id: int
    title: str
    description: str


@strawberry.input
class NoteInput:
    title: str
    description: str
