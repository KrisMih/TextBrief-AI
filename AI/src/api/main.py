from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from inference.predict import load_predictor
from inference.summarize import summarize_text


app = FastAPI(title="TextBrief AI")

#Load the trained model once when the API starts.
model, checkpoint = load_predictor()


class SummarizeRequest(BaseModel):
    text: str
    top_k: int = Field(default=2, ge=1, alias="topK")


@app.post("/summarize")
def summarize(request: SummarizeRequest):
    try:
        summary = summarize_text(
            request.text,
            model,
            checkpoint,
            top_k=request.top_k
        )

        return {"summary": summary}

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error