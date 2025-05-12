import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# ✅ Custom embedding wrapper
class SentenceTransformerEmbeddingFunction:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def __call__(self, texts):
        return self.model.encode(texts).tolist()

# ✅ Initialize Chroma client
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="chroma_db"
))

# ✅ Register collection with custom embedding (this prevents ONNX usage)
embedding_function = SentenceTransformerEmbeddingFunction()
collection = client.get_or_create_collection(
    name="etl_docs",
    embedding_function=embedding_function
)
