from typing import Optional

import chainlit as cl


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] == "ADMIN":
        return [
            cl.ChatProfile(
                name="GPT-3.5",
                markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            ),
            cl.ChatProfile(
                name="GPT-4",
                markdown_description="The underlying LLM model is **GPT-4**, a *1.5T parameter model* trained on 3.5TB of text data.",
                icon="https://picsum.photos/250",
            ),
            cl.ChatProfile(
                name="GPT-5",
                markdown_description="The underlying LLM model is **GPT-5**.",
                icon="https://picsum.photos/200",
            ),
        ]

    return [
        cl.ChatProfile(
            name="GPT-free",
            markdown_description="The underlying LLM model is **GPT-free**, a *1B parameter model* trained on 1TB of text data.",
        ),
        cl.ChatProfile(
            name="GPT-2",
            markdown_description="The underlying LLM model is **GPT-2**, a *1.5B parameter model* trained on 8TB of text data.",
        ),
    ]


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    match (username, password):
        case ("admin", "admin"):
            return cl.User(identifier="admin", metadata={"role": "ADMIN"})
        case ("user", "user"):
            return cl.User(identifier="user", metadata={"role": "USER"})
        case _:
            return None


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"starting chat with {user.identifier} using the {chat_profile} chat profile"
    ).send()
