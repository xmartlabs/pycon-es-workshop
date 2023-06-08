from fastapi import FastAPI

from schemas import EmbeddingsRequest, EmbeddingsResponse
from embedding_generator import EmbeddingsManager


app = FastAPI()


@app.post("/embedding", response_model=EmbeddingsResponse)
def get_embbeding_for_text(body: EmbeddingsRequest):
    emb_manger = EmbeddingsManager()
    embedding = emb_manger.get_embedding_sbert(body.text, body.type)
    return {'embedding': embedding}
