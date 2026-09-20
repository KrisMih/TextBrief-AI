# TextBrief-AI
> **Educational project:** TextBrief AI was created for learning and experimentation. It is not intended for production use.

# TextBrief AI

A small extractive text summarizer: a PyTorch model scores sentences, and the application selects two of them to form a summary.

**Stack:** Python, PyTorch, FastAPI, Java, Spring Boot, PostgreSQL, Flyway, JWT.

## Run locally

1. Start PostgreSQL and configure the existing database and JWT environment variables in `backend/.env`. Add `AI_BASE_URL=http://127.0.0.1:8000`.
2. Start the AI API from the `AI` directory:

   ```bash
   python -m pip install -r requirements.txt
   PYTHONPATH=src python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
   ```

3. Start the backend from the `backend` directory:

   ```bash
   set -a
   source .env
   set +a
   ./gradlew bootRun
   ```

The AI API uses a previously trained model checkpoint. If it is missing, run `PYTHONPATH=src python src/training/train.py` from the `AI` directory first.

## API

Authenticate using `POST /api/v1/auth/login`, then send the access token as `Authorization: Bearer <token>`.

**Create a summary:** `POST http://localhost:8080/api/v1/summaries/create`

```json
{
  "text": "Neural networks learn patterns from examples. A loss function measures prediction errors. The weather is sunny today."
}
```

**View your history:** `GET http://localhost:8080/api/v1/auth/summaries`

## Limitations

The model is a small educational sentence-ranking classifier, not a generative summarizer. It selects sentences from the input, was trained on a small dataset, and has a 10-token-per-sentence input limit in the current inference pipeline.
