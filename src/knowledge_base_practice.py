from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import DirectoryLoader
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from typing import List, Tuple

import json
import os

with open("config.json") as fptr:
    config = json.load(fptr)
    os.environ["OPENAI_API_KEY"]  = config["OPENAI_API_KEY"]
    os.environ["OPENAI_API_BASE"] = config["OPENAI_API_BASE"]

if __name__ == "__main__":
    # prepare knowledge base
    loader = DirectoryLoader(
        "src/data/knowledge_base/", glob="*.pdf", show_progress=True
    )
    docs = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    docs_split = text_splitter.split_documents(docs)

    # setup embedding
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()

    system_template = """
    Use the following pieces of context to answer the users question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Answering these questions in Chinese.
    -----------
    {question}
    -----------
    {chat_history}
    """

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo-16k")
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever, condense_question_prompt=prompt)
    chat_history: List[Tuple[str, str]] = []

    while True:
        question = input("问题：")
        result = qa_chain.invoke({"question": question, "chat_history": chat_history})
        chat_history.append((question, result["answer"]))
        print(result["answer"])
        print(type(result))