import streamlit as st

class MockPGVector:
    def __init__(self):
        # Mock database of historical project data
        self.mock_db = [
            {
                "id": 101,
                "project_name": "Solar Initiative Alpha",
                "content": "Previous solar panel installation in Region A faced a 2-week delay due to unexpected heavy rainfall.",
                "relevance_score": 0.92,
                "category": "Historical Risk"
            },
            {
                "id": 102,
                "project_name": "Wind Farm Beta",
                "content": "Stakeholders approved budget increase for turbine transportation logistics.",
                "relevance_score": 0.85,
                "category": "Historical Decision"
            },
            {
                "id": 103,
                "project_name": "Community Education",
                "content": "Educational workshops reached 500 local residents.",
                "relevance_score": 0.70,
                "category": "Historical Activity"
            }
        ]

    @st.cache_data
    def similarity_search(_self, query: str, top_k: int = 2):
        """
        Simulate a vector similarity search (RAG).
        In a real app, this would embed the query and search a vector DB.
        """
        query_lower = query.lower()
        results = []

        # Simple keyword matching to simulate semantic search
        for item in _self.mock_db:
            if "delay" in query_lower and "delay" in item["content"].lower():
                results.append(item)
            elif "solar" in query_lower and "solar" in item["content"].lower():
                results.append(item)
            elif "budget" in query_lower and "budget" in item["content"].lower():
                results.append(item)
            elif "education" in query_lower and "education" in item["content"].lower():
                results.append(item)

        # If no specific matches, return top results based on default mock scores
        if not results:
            sorted_db = sorted(_self.mock_db, key=lambda x: x['relevance_score'], reverse=True)
            results = sorted_db[:top_k]
        else:
            results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)[:top_k]

        return results
