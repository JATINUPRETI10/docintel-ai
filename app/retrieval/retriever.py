from config import TOP_K, FETCH_MULTIPLIER
from app.factories.components import get_vector_store


class Retriever:

    def __init__(self):
        self.vector_store = get_vector_store()

    def retrieve(self, query):

        # Fetch more candidates than needed
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=TOP_K * FETCH_MULTIPLIER
        )

        # No matches found
        if not results:
            return []

        documents = []
        seen = set()

        for doc, score in results:

            # Create a unique identifier for each chunk
            chunk_id = (
                doc.metadata.get("source", ""),
                doc.metadata.get("page", -1),
                hash(doc.page_content)
            )

            # Skip duplicate chunks
            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            # Store retrieval distance
            doc.metadata["score"] = round(float(score), 4)

            documents.append(doc)

            # Stop after collecting TOP_K unique chunks
            if len(documents) >= TOP_K:
                break

        return documents