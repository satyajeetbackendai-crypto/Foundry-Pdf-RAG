# Foundry PDF RAG with FastAPI (Module 4)

A small FastAPI app that answers questions from a **PDF document** using Microsoft Foundry (Azure OpenAI).

It is a simple teaching version of **RAG (Retrieval-Augmented Generation)**:

1. Read the PDF.
2. Find the parts that are relevant to the question.
3. Send only those parts to the model.
4. Get an answer based on the document.

## How it works

```
FastAPI  →  PDF  →  Retrieve context  →  Foundry  →  Answer
```

1. On startup, `documents/policy.pdf` is read into text.
2. `POST /ask` receives a question.
3. `get_context()` splits the text into chunks and scores each one by how many question words it contains.
4. The top 3 chunks go to the model as context, with the instruction to *answer using only the context*.
5. The model's answer is returned.

> **Note:** This retrieval uses keyword matching on purpose, to show the RAG idea without extra libraries. Module 5 replaces it with Azure AI Search for proper retrieval.

## Project structure

```
foundry-pdf-rag-fastapi/
├── app.py            # FastAPI app and prompt
├── rag.py            # PDF reading and context retrieval
├── requirements.txt
├── .env              # Your Azure keys (not committed)
├── .gitignore
└── documents/
    └── policy.pdf    # Sample company policy document
```

## Prerequisites

- Python 3.10+
- An Azure OpenAI / Microsoft Foundry resource with a chat model deployed (for example `gpt-4o`)

## Setup

1. **Open the project folder in VS Code**

2. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS/Linux, use `source .venv/bin/activate`.

3. **Install the dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project folder:

   ```env
   AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
   AZURE_OPENAI_API_KEY=YOUR_KEY
   AZURE_OPENAI_API_VERSION=2024-10-21
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   ```

   `AZURE_OPENAI_DEPLOYMENT` is the **deployment name** in Foundry, which may differ from the model name.

## Run

Run this from inside the project folder, because the PDF path is relative:

```powershell
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000/docs**, select **POST /ask**, then click **Try it out**.

## Try it

Request body:

```json
{
  "question": "How many days can employees work from home?"
}
```

Response:

```json
{
  "answer": "Employees can work from home up to 2 days per week."
}
```

Or use curl:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How many days can employees work from home?"}'
```

### Other questions to try

- How many days of paid annual leave do employees get?
- What are the standard office hours?
- What is the daily meal limit when travelling?
- When must a laptop be returned after leaving?

The sample PDF covers work from home, leave, office hours, expense and IT policies. For other topics, the model should say it doesn't have the information.

## Use your own PDF

Replace `documents/policy.pdf` with your own file and keep the same name, or change the path in `app.py`:

```python
document = read_pdf("documents/policy.pdf")
```

Retrieval splits the text on blank lines, so a PDF with clear sections or paragraphs works best.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `FileNotFoundError: documents/policy.pdf` | Start `uvicorn` from inside the project folder. |
| `404 Not Found` on `/ask` | A different app is running on port 8000. Stop it with Ctrl+C and start this one. |
| `'temperature' does not support 0 with this model` | Some models (o-series, GPT-5) accept only the default temperature. Don't pass `temperature`. |
| `401` / `Access denied` | Check `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in `.env`. |
| `DeploymentNotFound` | `AZURE_OPENAI_DEPLOYMENT` must match the deployment name in Foundry. |
