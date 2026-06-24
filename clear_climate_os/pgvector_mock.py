import math

class MockPGVectorDB:
    def __init__(self):
        # Mock database storing previous reports and their simulated embeddings
        self.documents = [
            {
                "id": 1,
                "text": "Solar panel installation faced delays due to heavy rains in early October.",
                "embedding": [0.1, 0.8, -0.2, 0.4]
            },
            {
                "id": 2,
                "text": "Community leaders requested additional training for local operators.",
                "embedding": [0.5, 0.1, 0.9, -0.1]
            },
            {
                "id": 3,
                "text": "Phase 2 budget was approved unanimously by the donor committee.",
                "embedding": [-0.3, 0.5, 0.2, 0.8]
            }
        ]

    def _cosine_similarity(self, v1, v2):
        dot_product = sum(a*b for a,b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a*a for a in v1))
        magnitude2 = math.sqrt(sum(b*b for b in v2))
        if magnitude1 * magnitude2 == 0:
            return 0
        return dot_product / (magnitude1 * magnitude2)

    def search(self, query_embedding, limit=2):
        """Simulate searching for similar documents using embeddings"""
        results = []
        for doc in self.documents:
            similarity = self._cosine_similarity(query_embedding, doc['embedding'])
            results.append((doc, similarity))

        # Sort by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

# Global instance for simulation
db = MockPGVectorDB()
