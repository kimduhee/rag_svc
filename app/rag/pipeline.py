class RAGPipeline:
    def __init__(self, embedder, store, llm):
        self.embedder = embedder
        self.store = store
        self.llm = llm

    def query(self, question):
        q_vec = self.embedder.embed([question])
        results = self.store.search(q_vec, k=3)

        context = ""
        images = []

        for r in results:
            context += r["data"]["content"] + "\n"
            images.extend([img["path"] for img in r["data"]["images"]])

        answer = self.llm.generate(context, images)

        return {
            "answer": answer,
            "images": images
        }
