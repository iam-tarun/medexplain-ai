from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from load_and_chunk import laod_and_chunk

def create_embeddings():
  chunks = laod_and_chunk()
  embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


  vectorstore = FAISS.from_documents(chunks, embedding)

  vectorstore.save_local("medexplain_faiss")


if __name__ == "__main__":
  create_embeddings()