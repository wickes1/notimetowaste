from fastapi import Depends, FastAPI, HTTPException, status
from langchain.schema import Document
from langchain_core.embeddings import Embeddings
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import VectorStore

from app.deps import get_chain, get_embedder, get_vector_store
from app.model import DocumentModel, DocumentResponse
from app.provider import AsyncPgVector

app = FastAPI(docs_url="/")


@app.post("/add-documents/", status_code=status.HTTP_201_CREATED)
async def add_documents(
    documents: list[DocumentModel],
    vector_store: VectorStore = Depends(get_vector_store),
    embedder: Embeddings = Depends(get_embedder),
):
    try:
        docs = [
            Document(
                page_content=doc.page_content,
                metadata=(
                    {
                        **doc.metadata,
                        "digest": doc.generate_digest(),
                    }
                ),
            )
            for doc in documents
        ]
        ids = (
            await vector_store.aadd_documents(docs)
            if isinstance(vector_store, AsyncPgVector)
            else vector_store.add_documents(docs)
        )
        return {"message": "Documents added successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-all-ids/")
async def get_all_ids(vector_store: VectorStore = Depends(get_vector_store)):
    try:
        if isinstance(vector_store, AsyncPgVector):
            ids = await vector_store.get_all_ids()
        else:
            ids = vector_store.get_all_ids()

        return ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-documents-by-ids/", response_model=list[DocumentResponse])
async def get_documents_by_ids(
    ids: list[str],
    vector_store: VectorStore = Depends(get_vector_store),
):
    try:
        if isinstance(vector_store, AsyncPgVector):
            existing_ids = await vector_store.get_all_ids()
            documents = await vector_store.get_documents_by_ids(ids)
        else:
            existing_ids = vector_store.get_all_ids()
            documents = vector_store.get_documents_by_ids(ids)

        if not all(id in existing_ids for id in ids):
            raise HTTPException(status_code=404, detail="Some documents not found")

        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-documents/")
async def delete_documents(
    ids: list[str],
    vector_store: VectorStore = Depends(get_vector_store),
):
    try:
        if isinstance(vector_store, AsyncPgVector):
            existing_ids = await vector_store.get_all_ids()
            await vector_store.delete(ids=ids)
        else:
            existing_ids = vector_store.get_all_ids()
            vector_store.delete(ids=ids)

        if not all(id in existing_ids for id in ids):
            raise HTTPException(status_code=404, detail="Some documents not found")

        return {"message": "Documents deleted successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(msg: str, chain: Runnable = Depends(get_chain)):
    return chain.invoke(msg)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
