from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI as LangChainOpenAI
from backend import config, vector_store

def answer_query(query, vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    system_prompt = (
        "You are an expert assistant for Venkata Ramana Reddy's resume and project portfolio. "
        "Always answer in a helpful, concise, and professional manner. "
        "If you do not know the answer, say 'I do not know based on the provided information.'"
    )
    full_prompt = f"{system_prompt}\n\nUser question: {query}"
    qa_chain = RetrievalQA.from_chain_type(
        llm=LangChainOpenAI(temperature=0.3, openai_api_key=config.OPENAI_API_KEY),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain(full_prompt)
    print("Retrieved docs:", result.get("source_documents"))
    return result["result"]