import requests
from typing import List, Dict, Any, Optional

class DataTestLibrary:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_mission_analytics(self) -> Dict[str, Any]:
        """Fetch mission analytics from the API"""
        response = requests.get(f"{self.base_url}/analytics")
        response.raise_for_status()
        return response.json()

    def add_security_policy(self, policy_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a security policy via the API"""
        payload = {
            "id": policy_id,
            "content": content,
            "metadata": metadata or {}
        }
        response = requests.post(f"{self.base_url}/policies", json=payload)
        response.raise_for_status()
        return response.json()

    def list_security_policies(self) -> List[str]:
        """List all security policies via the API"""
        response = requests.get(f"{self.base_url}/policies")
        response.raise_for_status()
        return response.json()["policies"]

    def search_security_policies(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """Search security policies via the API"""
        payload = {
            "query": query,
            "n_results": n_results
        }
        response = requests.post(f"{self.base_url}/policies/search", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_security_policy(self, policy_id: str):
        """Delete a security policy via the API"""
        response = requests.delete(f"{self.base_url}/policies/{policy_id}")
        response.raise_for_status()
        return response.json()
