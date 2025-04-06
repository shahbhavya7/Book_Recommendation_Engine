from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


db_books = Chroma(persist_directory="db", embedding_function=embedding_model)

query = "Find books about nature"
results = db_books.similarity_search(query, k=5)  

# Print results
for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(doc.page_content)
    print("-" * 50)
