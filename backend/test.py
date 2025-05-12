import chromadb
client = chromadb.Client()
collection = client.create_collection("test_collection")
collection.add(documents=["Hello world"], ids=["doc1"])
results = collection.query(query_texts=["Hello"], n_results=1)
print(results)