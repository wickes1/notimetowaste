import chainlit as cl
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.callbacks import CallbackManager
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.service_context import ServiceContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


@cl.on_chat_start
async def on_chat_start():
    Settings.llm = Ollama(
        base_url="http://localhost:11434",
        model="llama3:8b-instruct-q6_K",
        temperature=0.1,
        max_tokens=1024,
        streaming=True,
    )
    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url="http://localhost:11434",
        ollama_additional_kwargs={"mirostat": 0},
    )
    Settings.context_window = 4096

    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    except FileNotFoundError:
        documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist()

    # service_context = ServiceContext.from_defaults(
    #     callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()])
    # )
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=2,
    )
    cl.user_session.set("query_engine", query_engine)

    await cl.Message(
        author="Assistant", content="Hello! Im an AI assistant. How may I help you?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")  # type: RetrieverQueryEngine

    msg = cl.Message(content="", author="Assistant")

    res = await cl.make_async(query_engine.query)(message.content)

    for token in res.response_gen:
        await msg.stream_token(token)
    await msg.send()
