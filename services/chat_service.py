# services/chat_service.py
from elasticsearch import Elasticsearch
from services.llm_service import correct_text_with_llm

# Initialize ElasticSearch client (configure host/port as needed).
es = Elasticsearch(hosts=["http://localhost:9200"])

def index_pdf_content(doc_id: str, markdown_text: str, metadata: dict):
    """
    Index PDF content and its metadata into ElasticSearch.
    """
    document = {
        "markdown": markdown_text,
        "metadata": metadata
    }
    es.index(index="pdf_contents", id=doc_id, document=document)

def search_pdf_contents(query: str) -> list:
    """
    Search the indexed PDF contents in ElasticSearch for relevant sections.
    """
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["markdown", "metadata.*"]
            }
        }
    }
    results = es.search(index="pdf_contents", body=body)
    return [hit["_source"] for hit in results["hits"]["hits"]]

def generate_chat_response(user_query: str, retrieved_docs: list) -> str:
    """
    Combine user query and retrieved documents to generate a cohesive response.
    This can integrate with LangChain or your LLM.
    """
    # For demonstration, we just concatenate the texts.
    context = "\n\n".join(doc.get("markdown", "") for doc in retrieved_docs)
    prompt = f"Context:\n{context}\n\nUser Query: {user_query}\n\nResponse:"
    # Here you would send the prompt to your LLM.
    response = correct_text_with_llm(prompt)  # reusing our LLM function as an example.
    return response

def query_chatbot(user_query: str) -> dict:
    """
    Orchestrate the search and chat response.
    """
    relevant_docs = search_pdf_contents(user_query)
    response = generate_chat_response(user_query, relevant_docs)
    return {"response": response, "retrieved_docs": relevant_docs}
