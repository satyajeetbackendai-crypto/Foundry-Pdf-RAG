import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
from rag import read_pdf, get_context

load_dotenv()

app = FastAPI()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")

document = read_pdf("documents/policy.pdf")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(request: Question):
    context = get_context(
        document,
        request.question
    )

    prompt = f"""
Answer using only the context.

Context:
{context}

Question:
{request.question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }
