from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

raw_documents = TextLoader("tagged_description.txt", encoding="utf-8").load()
text_splitter = CharacterTextSplitter(chunk_size=0, chunk_overlap=0, separator="\n")
documents = text_splitter.split_documents(raw_documents)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create a persistent Chroma DB (specify persist directory)
db_books = Chroma.from_documents(documents, embedding=embedding_model, persist_directory="db")

# Save embeddings
db_books.persist()