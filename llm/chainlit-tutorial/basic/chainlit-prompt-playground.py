import chainlit as cl
from chainlit.input_widget import Select
from chainlit.playground.providers import ChatOpenAI
from openai import AsyncOpenAI

client = AsyncOpenAI()

template = "Hello, {name}!"
variables = {
    "name": "John",
}

settings = {
    "model": "llama3:8b-instruct-q6_K",
    "temperature": 0,
    # ... more settings
}


@cl.step(type="llm")
async def call_llm():
    generation = cl.ChatGeneration(
        provider=ChatOpenAI.id,
        variables=variables,
        settings=settings,
        messages=[
            {"content": template.format(**variables), "role": "user"},
        ],
    )

    # Make the call to OpenAI
    response = await client.chat.completions.create(
        messages=generation.messages, **settings
    )

    generation.message_completion = {
        "content": response.choices[0].message.content,
        "role": "assistant",
    }

    # Add the generation to the current step
    cl.context.current_step.generation = generation

    return generation.message_completion["content"]


@cl.on_chat_start
async def start():
    await call_llm()
