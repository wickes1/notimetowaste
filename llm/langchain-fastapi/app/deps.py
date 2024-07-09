from functools import lru_cache

from langchain_core.runnables import Runnable

from app.config import settings


@lru_cache
def get_embedder():
    from langchain_community.embeddings.ollama import OllamaEmbeddings

    return OllamaEmbeddings(model="nomic-embed-text")


@lru_cache
def get_vector_store():
    match settings.VECTOR_STORE_MODE:
        case "sync":
            from app.provider import ExtendedPgVector

            return ExtendedPgVector(
                connection_string=settings.DB_CONN.unicode_string(),
                embedding_function=get_embedder(),
                collection_name="testcollection",
            )
        case "async":
            from app.provider import AsyncPgVector

            return AsyncPgVector(
                connection_string=settings.DB_CONN.unicode_string(),
                embedding_function=get_embedder(),
                collection_name="testcollection",
            )
        case _:
            raise ValueError("Invalid VECTOR_STORE_MODE")


@lru_cache
def get_prompt():
    from langchain_core.prompts import ChatPromptTemplate

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    return ChatPromptTemplate.from_template(template)


@lru_cache
def get_chain() -> Runnable:
    from langchain_community.chat_models.ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    retriever = get_vector_store().as_retriever()
    prompt = get_prompt()
    model = ChatOllama(model_name="dolphin-mistral")
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
