from fastapi import APIRouter
from langchain_ollama import ChatOllama,OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


llm = ChatOllama(
    model="minimax-m3:cloud",
    temperature=0
)



router=APIRouter(
    prefix="/query",
    tags=['query'],
)



embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="first_collection",
    url="http://localhost:6333"
)


@router.post("/")
async def query(question: str):
    # Retrieve relevant documents
    search_result = vector_db.similarity_search(query=question)

    print(f"Search result for '{question}':\n{search_result}")

    # Build context
    context = "\n\n".join(
        
        f"""
        Page: {doc.metadata.get('page')}

        Content:
        {doc.page_content}
        """
            for doc in search_result
        )

    # System Prompt
    system_prompt = """
    You are a Retrieval-Augmented Generation assistant.

    Answer ONLY using the retrieved context.

    If the answer is not in the context, say:
    "I couldn't find the answer in the provided documents."

    Do not use outside knowledge.
    """
    user_prompt = f"""
    Retrieved Context:

    {context}

    Question:
    {question}
    """

    # Messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Invoke LLM
    response = llm.invoke(messages)

    unique_pages = sorted(
        {
            doc.metadata.get("page")
            for doc in search_result
            if doc.metadata.get("page") is not None})

    return {
    "question": question,
    "answer": response.content,
    "sources": {
        "document": search_result[0].metadata.get("source") if search_result else None,
        "pages": unique_pages,
    },
}