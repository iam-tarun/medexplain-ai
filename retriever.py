from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def getRetriever():
  embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  vectorstore = FAISS.load_local("medexplain_faiss", embeddings=embedding)

  retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

  return retriever