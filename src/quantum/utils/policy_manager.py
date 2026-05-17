import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os

class PolicyManager:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="mission_policies")

    def add_policy(self, policy_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a security policy to the vector store"""
        self.collection.add(
            documents=[content],
            metadatas=[metadata] if metadata else [{}],
            ids=[policy_id]
        )

    def search_policies(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """Search for semantically similar policies"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def list_policies(self) -> List[str]:
        """List all policy IDs"""
        return self.collection.get()["ids"]

    def delete_policy(self, policy_id: str):
        """Delete a policy by ID"""
        self.collection.delete(ids=[policy_id])
