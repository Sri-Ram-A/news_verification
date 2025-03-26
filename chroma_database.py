import chromadb
from typing import List, Dict
from datetime import datetime

class ChromaDB:
    def __init__(self, collection_name: str):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": f"Chroma collection for:{collection_name}",
                "created": str(datetime.now())
                } 
            )

    def add_data(self,):
        
        pass
    def query_documents(self, query_text: str, n_results: int = 2):
        return self.collection.query(query_texts=[query_text], n_results=n_results)

# Example Usage
if __name__ == "__main__":
    db_handler = ChromaDB("my_collection")
    
    documents = ["This is a document about pineapple", "This is a document about oranges"]
    embeddings = [[1.1, 2.3, 3.2], [4.5, 6.9, 4.4]]
    metadata = [{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}]
    
    db_handler.insert_documents(documents, embeddings, metadata)
    
    results = db_handler.query_documents("This is a query document about Florida", n_results=2)
    print(results)